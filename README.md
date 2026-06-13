# 留白 (Liubai)

> 予一席空白 — 轻量个人博客，Markdown 写作，话题归档，移动端友好。

[![GitHub](https://img.shields.io/github/repo/honkerc/liubai?style=flat-square)](https://github.com/honkerc/liubai)

**留白** 是一套前后端分离的个人博客系统：前端 Vue 3 负责阅读与编辑体验，后端 FastAPI 提供 REST API、鉴权与文件上传。界面克制、留白充足，适合长期写作与归档。

---

## 功能特性

| 模块 | 说明 |
|------|------|
| **文章** | Markdown 撰写与渲染，标题即 URL，草稿 / 发布状态，置顶 |
| **话题** | 多话题标签，按话题浏览与筛选 |
| **搜索** | 全文搜索，关键词高亮 |
| **侧边栏** | 文章列表、快捷入口（话题 / 搜索 / 写作 / 登录） |
| **编辑器** | 实时预览、图片 / 视频上传、本地草稿自动保存 |
| **移动端** | 响应式布局，顶栏居中展示品牌 Logo + 站名 |
| **部署** | 支持开发热重载、Docker 单容器、Nginx + systemd 生产方案 |

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3、Vue Router、Marked、Highlight.js |
| 后端 | FastAPI、Uvicorn、Tortoise ORM |
| 数据库 | SQLite |
| 鉴权 | JWT（Bearer Token） |
| 部署 | Docker、Nginx、systemd |

---

## 项目结构

```
liubai/
├── backend/              # FastAPI 后端
│   ├── main.py           # 应用入口与 API 路由
│   ├── auth.py           # 登录与 JWT
│   ├── models.py         # 数据模型
│   ├── config.py         # 环境变量与路径配置
│   ├── upload_service.py # 文件上传
│   └── requirements.txt
├── frontend/             # Vue 3 前端
│   ├── public/           # 静态资源（favicon cat.svg）
│   ├── src/
│   │   ├── components/   # 布局、侧边栏、编辑器组件
│   │   ├── views/        # 页面视图
│   │   ├── constants/    # 品牌配置 brand.js
│   │   └── utils/        # 工具函数
│   └── package.json
├── deploy/               # Nginx、systemd、环境变量示例
├── scripts/              # 构建与部署脚本
├── start.py              # 本地一键启动（前后端）
├── Dockerfile            # Docker 多阶段构建
├── docker-compose.yml
├── DEPLOY.md             # 生产部署详细说明
└── README.md
```

---

## 快速开始（开发）

### 环境要求

- **Python** 3.10+
- **Node.js** 18+ 与 npm
- Windows / macOS / Linux 均可

### 1. 克隆仓库

```bash
git clone https://github.com/honkerc/liubai.git
cd liubai
```

### 2. 后端

```bash
cd backend
pip install -r requirements.txt

# 可选：复制并编辑环境变量
cp .env.example .env

# 启动（开发模式，热重载）
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/api/health

### 3. 前端

新开一个终端：

```bash
cd frontend
npm install
npm run serve
```

访问 http://localhost:8080 。开发环境下 `/api` 与 `/uploads` 会通过 `vue.config.js` 代理到后端 8000 端口。

### 4. 一键启动（推荐）

在项目根目录：

```bash
python start.py
```

会分别打开后端（8000）与前端（8080）进程，日志写入 `logs/` 目录：

```bash
python view_logs.py          # 查看最近日志
python view_logs.py -f       # 实时跟踪
python view_logs.py backend  # 仅后端
```

---

## 默认账号

首次启动时，后端会根据环境变量创建管理员账号：

| 变量 | 默认值 |
|------|--------|
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | `admin123` |

**生产环境务必修改** `SECRET_KEY`、`ADMIN_PASSWORD`。配置方式见下方「环境变量」。

---

## 环境变量

### 后端（`backend/.env`）

开发时复制 `backend/.env.example` 为 `backend/.env`：

```env
SECRET_KEY=change-me-to-a-long-random-string
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-me
HOST=127.0.0.1
PORT=8000
```

| 变量 | 说明 |
|------|------|
| `SECRET_KEY` | JWT 签名密钥，生产必改 |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | 管理员账号 |
| `DATA_DIR` | 数据目录（SQLite、`uploads/`），默认 `backend/` |
| `DATABASE_NAME` | 数据库文件名，默认 `db.sqlite3` |
| `SERVE_STATIC` | 是否由后端托管前端静态文件（Docker / 本地验证用） |
| `STATIC_DIR` | 前端 `dist` 目录路径 |
| `CORS_ORIGINS` | 允许的跨域来源，逗号分隔 |

### 前端

生产构建时 `VUE_APP_API_BASE` 留空表示与站点同域（Nginx 反代 `/api`）。开发环境无需配置，走 devServer 代理。

---

## 生产部署

### 方式一：Nginx + systemd（推荐）

详见 [DEPLOY.md](./DEPLOY.md)。

```bash
# Linux 服务器上一键部署
sudo DOMAIN=blog.example.com ./scripts/deploy-nginx.sh
```

默认安装目录 `/www/blog`，上传目录 `/www/uploads/`，数据库 `/www/db.sqlite3`，环境变量 `/etc/blog/env`。

### 方式二：Docker

```bash
cp .env.example .env
# 编辑 .env 中的 SECRET_KEY、ADMIN_PASSWORD

docker compose up -d --build
```

访问 http://localhost:8000（前后端同容器、同端口）。

### 方式三：本地生产验证

不装 Nginx，构建前端并由后端托管：

```bash
python scripts/run-prod.py
```

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `python start.py` | 开发：同时启动前后端 |
| `npm run serve` | 仅前端开发服务器 |
| `npm run build` | 构建前端到 `frontend/dist/` |
| `bash scripts/build-release.sh` | 构建生产前端包 |
| `python scripts/run-prod.py` | 本地生产模式验证 |
| `docker compose up -d --build` | Docker 部署 |

---

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/auth/login` | 登录，返回 JWT |
| GET | `/api/articles` | 文章列表（分页、搜索、话题筛选） |
| GET | `/api/articles/all` | 侧边栏用全量列表 |
| GET | `/api/articles/by-title/{title}` | 按标题获取文章 |
| POST | `/api/articles` | 创建文章（需登录） |
| PUT | `/api/articles/{id}` | 更新文章（需登录） |
| DELETE | `/api/articles/{id}` | 删除文章（需登录） |
| GET | `/api/topics` | 话题列表 |
| POST | `/api/upload` | 上传图片 / 视频（需登录） |

完整接口见 Swagger：http://127.0.0.1:8000/docs

---

## 品牌定制

站点名称、副标题、Logo 集中在 `frontend/src/constants/brand.js`：

```javascript
export const SITE_NAME = '留白'
export const SITE_TAGLINE = '予一席空白'
export const SITE_LOGO = `${process.env.BASE_URL}cat.svg`
```

替换 `frontend/public/cat.svg` 即可更换 favicon 与侧边栏 Logo。

---

## 开发说明

- 后端仅加载 `backend/.env`，不会误读项目根目录的 Docker 用 `.env`。
- 若 `DATA_DIR` 指向空库而 `backend/db.sqlite3` 有旧数据，会自动回退到旧库（迁移兼容）。
- 前端路由使用 History 模式，Nginx 需配置 `try_files` 回退到 `index.html`（见 `deploy/nginx.conf`）。

---

## 许可证

本项目为个人博客项目，可按需 fork 与修改。

---

## 链接

- 仓库：https://github.com/honkerc/liubai
- 部署文档：[DEPLOY.md](./DEPLOY.md)
