from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q
from typing import List, Optional

from tortoise import Tortoise

import os
from pathlib import Path
from auth import router as auth_router, get_current_user, get_current_user_optional
from config import (
    API_VERSION,
    BUILD_TIME,
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    CORS_ORIGINS,
    DATABASE_PATH,
    SERVE_STATIC,
    STATIC_DIR,
)
from models import User, Article
from schemas import ArticleCreate, ArticleUpdate, ArticleOut, UploadOut
from upload_service import UPLOAD_ROOT, ensure_upload_dirs, save_upload, cleanup_uploads_if_needed


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path = str(DATABASE_PATH)
    migrate_article_is_pinned(db_path)
    await Tortoise.init(
        db_url=f"sqlite://{db_path}",
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()
    await migrate_article_title_unique(db_path)

    from passlib.hash import bcrypt

    admin, created = await User.get_or_create(
        username=ADMIN_USERNAME,
        defaults={
            "password_hash": bcrypt.hash(ADMIN_PASSWORD),
        },
    )
    if created:
        print(f"[OK] 默认管理员已创建: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")

    os.makedirs(UPLOAD_ROOT, exist_ok=True)
    ensure_upload_dirs()
    cleanup_uploads_if_needed()

    yield

    await Tortoise.close_connections()


app = FastAPI(
    title="留白",
    description="个人博客",
    version=API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


# ===== 数据库迁移 =====

async def migrate_article_title_unique(db_path: str):
    """去重标题：同标题保留最新一篇，删除其余；并确保 title 唯一索引"""
    import sqlite3
    from collections import defaultdict

    articles = await Article.all().order_by("-updated_at", "-created_at")
    groups = defaultdict(list)
    for article in articles:
        title = (article.title or "").strip() or "未命名"
        if title != article.title:
            article.title = title
            await article.save(update_fields=["title"])
        groups[title].append(article)

    removed = 0
    for title, group in groups.items():
        if len(group) <= 1:
            continue
        for duplicate in group[1:]:
            await duplicate.delete()
            removed += 1

    if removed:
        print(f"[OK] 已清理 {removed} 篇重复标题文章")

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_articles_title_unique ON articles(title)"
        )
        conn.commit()
    except sqlite3.IntegrityError as exc:
        print(f"[WARN] title 唯一索引未创建: {exc}")
    finally:
        conn.close()


def migrate_article_is_pinned(db_path: str):
    """为 articles 表添加 is_pinned 列（已有库兼容）"""
    import sqlite3

    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    try:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        if "articles" not in tables:
            return

        cols = {row[1] for row in conn.execute("PRAGMA table_info(articles)").fetchall()}

        # 修复误带引号的列名（会导致 Tortoise KeyError: '"is_pinned"'）
        for bad_name in ('"is_pinned"', "'is_pinned'"):
            if bad_name in cols and "is_pinned" not in cols:
                quoted = '"' + bad_name.replace('"', '""') + '"'
                conn.execute(
                    f"ALTER TABLE articles RENAME COLUMN {quoted} TO is_pinned"
                )
                conn.commit()
                print(f"[OK] 已修复 articles 列名: {bad_name} -> is_pinned")
                cols.discard(bad_name)
                cols.add("is_pinned")

        if "is_pinned" not in cols:
            conn.execute(
                "ALTER TABLE articles ADD COLUMN is_pinned INTEGER NOT NULL DEFAULT 0"
            )
            conn.commit()
            print("[OK] 已添加 articles.is_pinned 列")
    finally:
        conn.close()


def _article_order():
    return ("-is_pinned", "-created_at")


async def _save_article_fields(article: Article, *, content: str, topic: str, is_published: bool, is_pinned: bool) -> Article:
    article.content = content
    article.topic = topic
    article.is_published = is_published
    article.is_pinned = is_pinned
    await article.save()
    return article


async def _upsert_article_by_title(title: str, data: ArticleCreate, author: User) -> Article:
    """按标题创建或更新文章，避免重复标题导致 500"""
    existing = await Article.filter(title=title).first()
    if existing:
        return await _save_article_fields(
            existing,
            content=data.content,
            topic=data.topic,
            is_published=data.is_published,
            is_pinned=data.is_pinned,
        )

    try:
        return await Article.create(
            author=author,
            title=title,
            content=data.content,
            topic=data.topic,
            is_published=data.is_published,
            is_pinned=data.is_pinned,
        )
    except IntegrityError:
        existing = await Article.filter(title=title).first()
        if existing:
            return await _save_article_fields(
                existing,
                content=data.content,
                topic=data.topic,
                is_published=data.is_published,
                is_pinned=data.is_pinned,
            )
        raise HTTPException(status_code=409, detail="标题已存在")


def _updated_at_matches(stored, expected) -> bool:
    if stored is None or expected is None:
        return False
    stored_naive = stored.replace(tzinfo=None) if hasattr(stored, "replace") else stored
    expected_naive = expected.replace(tzinfo=None) if hasattr(expected, "replace") else expected
    return stored_naive == expected_naive


# ===== 文章 API =====

async def title_taken(title: str, exclude_id=None) -> bool:
    query = Article.filter(title=title.strip())
    if exclude_id is not None:
        query = query.exclude(id=exclude_id)
    return await query.exists()


@app.get("/api/articles", response_model=List[ArticleOut])
async def list_articles(
    search: Optional[str] = Query(None, description="搜索标题和内容"),
    topic: Optional[str] = Query(None, description="按话题筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """公开接口：获取已发布的文章列表"""
    query = Article.filter(is_published=True)

    if search:
        query = query.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )

    if topic:
        query = query.filter(topic=topic)

    articles = await (
        query.order_by(*_article_order())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    return articles


@app.get("/api/articles/all", response_model=List[ArticleOut])
async def list_all_articles(
    current_user: User = Depends(get_current_user),
):
    """管理接口：获取所有文章（包括草稿）"""
    articles = await Article.all().order_by(*_article_order())
    return articles


@app.get("/api/articles/by-title/{title}", response_model=ArticleOut)
async def get_article_by_title(
    title: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """通过标题获取文章（公开；登录用户可查看草稿）"""
    article = await Article.filter(title=title).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    if not article.is_published and current_user is None:
        raise HTTPException(status_code=404, detail="文章不存在")

    if article.is_published and current_user is None:
        article.views += 1
        await article.save(update_fields=["views"])

    return article


@app.get("/api/articles/{article_id}", response_model=ArticleOut)
async def get_article(
    article_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """获取单篇文章（公开；登录用户可查看草稿）"""
    try:
        article = await Article.get(id=article_id)
    except Exception:
        raise HTTPException(status_code=404, detail="文章不存在")

    if not article.is_published and current_user is None:
        raise HTTPException(status_code=404, detail="文章不存在")

    if article.is_published and current_user is None:
        article.views += 1
        await article.save(update_fields=["views"])

    return article


@app.post("/api/articles", response_model=ArticleOut, status_code=201)
async def create_article(data: ArticleCreate, current_user: User = Depends(get_current_user)):
    """创建文章；标题唯一，已存在则更新该文章"""
    title = data.title.strip()
    return await _upsert_article_by_title(title, data, current_user)


@app.put("/api/articles/{article_id}", response_model=ArticleOut)
async def update_article(article_id: str, data: ArticleUpdate, current_user: User = Depends(get_current_user)):
    try:
        article = await Article.get(id=article_id)
    except Exception:
        raise HTTPException(status_code=404, detail="文章不存在")

    update_data = data.model_dump(exclude_unset=True)
    expected_updated_at = update_data.pop("expected_updated_at", None)
    if expected_updated_at is not None and not _updated_at_matches(article.updated_at, expected_updated_at):
        raise HTTPException(status_code=409, detail="文章已在其他窗口更新，请刷新后重试")

    if "title" in update_data and update_data["title"] is not None:
        title = update_data["title"].strip()
        update_data["title"] = title
        if await title_taken(title, exclude_id=article_id):
            raise HTTPException(status_code=409, detail="标题已存在")

    if update_data:
        try:
            await article.update_from_dict(update_data)
            await article.save()
        except IntegrityError:
            raise HTTPException(status_code=409, detail="标题已存在")

    return article


@app.delete("/api/articles/{article_id}")
async def delete_article(article_id: str, current_user: User = Depends(get_current_user)):
    try:
        article = await Article.get(id=article_id)
    except Exception:
        raise HTTPException(status_code=404, detail="文章不存在")

    await article.delete()
    return {"message": "文章已删除"}


@app.get("/api/topics")
async def list_topics():
    """获取所有话题（去重）"""
    articles = await Article.filter(is_published=True).values_list("topic", flat=True)
    topics = set()
    for t in articles:
        if t and t.strip():
            topics.add(t.strip())
    return sorted(topics)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "message": "留白 API",
        "version": API_VERSION,
        "build_time": BUILD_TIME,
    }


if not SERVE_STATIC:
    @app.get("/")
    async def root():
        return {
            "message": "留白 API",
            "version": API_VERSION,
            "build_time": BUILD_TIME,
            "health": "/api/health",
        }


@app.post("/api/upload", response_model=UploadOut)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """上传文件：图片保存原图并生成压缩版，其他文件正常保存"""
    result = await save_upload(file)
    cleanup_uploads_if_needed()
    return result


ensure_upload_dirs()
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_ROOT)), name="uploads")


def _mount_frontend(app: FastAPI) -> None:
    if not SERVE_STATIC:
        return

    static_root = Path(STATIC_DIR) if STATIC_DIR else None
    if not static_root or not static_root.is_dir():
        print(f"[WARN] SERVE_STATIC=true 但 STATIC_DIR 无效: {STATIC_DIR!r}")
        return

    class SPAStaticFiles(StaticFiles):
        async def get_response(self, path: str, scope):
            try:
                return await super().get_response(path, scope)
            except StarletteHTTPException as exc:
                if exc.status_code == 404:
                    return await super().get_response("index.html", scope)
                raise exc

    app.mount("/", SPAStaticFiles(directory=str(static_root), html=True), name="spa")
    print(f"[OK] 前端静态资源已托管: {static_root}")


_mount_frontend(app)
