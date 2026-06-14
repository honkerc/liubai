"""应用配置（支持环境变量）"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

try:
    from dotenv import load_dotenv

    # 仅加载后端目录下的 .env，避免误读项目根目录的 Docker 配置
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass


def _resolve_data_dir() -> Path:
    explicit = os.getenv("DATA_DIR", "").strip()
    if explicit:
        return Path(explicit).resolve()
    return BASE_DIR


DATA_DIR = _resolve_data_dir()

# 兼容：旧数据在 backend/ 下，勿误用空的 data/ 目录
_legacy_db = BASE_DIR / "db.sqlite3"
_current_db = DATA_DIR / os.getenv("DATABASE_NAME", "db.sqlite3")
if (
    DATA_DIR != BASE_DIR
    and _legacy_db.is_file()
    and (not _current_db.is_file() or _current_db.stat().st_size < 8192)
):
    DATA_DIR = BASE_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)

API_VERSION = os.getenv("API_VERSION", "1.0.0")
BUILD_TIME = os.getenv("BUILD_TIME") or datetime.fromtimestamp(
    Path(__file__).stat().st_mtime, tz=timezone.utc
).isoformat()

SECRET_KEY = os.getenv("SECRET_KEY", "liubai-blog-secret-key-change-in-production")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

DATABASE_PATH = DATA_DIR / os.getenv("DATABASE_NAME", "db.sqlite3")


def _resolve_upload_root() -> Path:
    explicit = os.getenv("UPLOAD_DIR", "").strip()
    if explicit:
        return Path(explicit).resolve()
    return DATA_DIR / "uploads"


UPLOAD_ROOT = _resolve_upload_root()
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

STATIC_DIR = os.getenv("STATIC_DIR", "").strip()
SERVE_STATIC = os.getenv("SERVE_STATIC", "").lower() in ("1", "true", "yes")

_default_cors = "http://localhost:8080,http://127.0.0.1:8080,http://localhost:8081,http://127.0.0.1:8081,http://localhost:8000,http://127.0.0.1:8000"
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", _default_cors).split(",")
    if origin.strip()
]

UPLOAD_DIR_MAX_BYTES = int(os.getenv("UPLOAD_DIR_MAX_BYTES", str(2 * 1024 * 1024 * 1024)))
