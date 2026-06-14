# 留白 部署说明

个人博客 **留白**（FastAPI + Vue 3）。生产环境推荐 **Nginx + systemd**，默认安装目录 **`/www/liubai`**。

## 架构

```
用户 → Nginx (:80 / :443)
         ├─ /              → /www/liubai/frontend/dist（SPA）
         ├─ /uploads/      → /www/liubai/uploads/
         └─ /api/          → 127.0.0.1:8000

systemd: blog.service → uvicorn（SERVE_STATIC=false）
```

| 路径 | 用途 |
|------|------|
| `/www/liubai` | 项目代码、`.venv` |
| `/www/liubai/backend` | FastAPI 工作目录 |
| `/www/liubai/frontend/dist` | 前端静态文件（Nginx root） |
| `/www/liubai/uploads/` | 上传文件 |
| `/www/liubai/db.sqlite3` | SQLite 数据库 |
| `/etc/blog/env` | 后端环境变量 |

## 一键部署

```bash
sudo DOMAIN=blog.example.com ./scripts/deploy-nginx.sh
```

编辑 `/etc/blog/env`，修改 `SECRET_KEY`、`ADMIN_PASSWORD` 后：

```bash
sudo systemctl restart blog
sudo certbot --nginx -d blog.example.com   # 可选 HTTPS
```

## 手动步骤

```bash
./scripts/build-release.sh
sudo mkdir -p /www/liubai /www/liubai/uploads /www/liubai/frontend/dist
# rsync 代码到 /www/liubai，安装 venv 与依赖
sudo cp deploy/env.example /etc/blog/env
sudo cp deploy/blog.service /etc/systemd/system/
sudo cp deploy/nginx.conf /etc/nginx/sites-available/blog
sudo systemctl enable --now blog
sudo nginx -t && sudo systemctl reload nginx
```

## 运维

```bash
systemctl status blog
journalctl -u blog -f
curl http://127.0.0.1:8000/api/health
```

更新：在 `/www/liubai` 拉代码后重新执行 `deploy-nginx.sh`。

## Docker（可选）

```bash
cp .env.example .env
docker compose up -d --build
```

## 开发

```bash
python start.py
```

## 环境变量

见 `deploy/env.example`。Nginx 部署时 `DATA_DIR=/www/liubai`（库在 `/www/liubai/db.sqlite3`，上传在 `/www/liubai/uploads/`），`SERVE_STATIC=false`。

## 上线检查

- [ ] `SECRET_KEY`、`ADMIN_PASSWORD` 已修改
- [ ] Nginx 域名与路径正确
- [ ] `systemctl status blog` 为 active
- [ ] 首页、登录、上传正常
