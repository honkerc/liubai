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
| `/www/liubai/backend/.env` | 后端环境变量 |

## 一键部署

```bash
sudo DOMAIN=blog.example.com ./scripts/deploy-nginx.sh
```

编辑 `/www/liubai/backend/.env`，修改 `SECRET_KEY`、`ADMIN_PASSWORD` 后：

```bash
sudo systemctl restart blog
sudo certbot --nginx -d blog.example.com   # 可选 HTTPS
```

## 手动步骤

```bash
./scripts/build-release.sh
sudo mkdir -p /www/liubai /www/liubai/uploads /www/liubai/frontend/dist
# rsync 代码到 /www/liubai，安装 venv 与依赖
sudo cp backend/.env.example /www/liubai/backend/.env
sudo chmod 600 /www/liubai/backend/.env
sudo cp deploy/blog.service /etc/systemd/system/
sudo cp deploy/nginx.conf /etc/nginx/sites-available/blog
sudo systemctl enable --now blog
sudo nginx -t && sudo systemctl reload nginx
```

## 运维

```bash
systemctl status liubai    # 或 blog
journalctl -u liubai -n 80 --no-pager
curl http://127.0.0.1:8000/api/health
```

### 服务启动失败（exit-code 3）

1. **看日志**（最重要）：

```bash
sudo journalctl -u liubai -n 80 --no-pager
```

2. **用 www-data 手动跑**（复现错误）：

```bash
cd /www/liubai/backend
sudo -u www-data /www/liubai/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
```

3. **常见原因**

| 原因 | 处理 |
|------|------|
| 未装 venv / 依赖 | `cd /www/liubai && python3 -m venv .venv && .venv/bin/pip install -r backend/requirements.txt` |
| `backend/.env` 缺失 | `sudo cp backend/.env.example /www/liubai/backend/.env` 并修改密钥 |
| **www-data 无法写数据目录** | 见下方权限 |
| 8000 端口被占用 | `sudo ss -tlnp \| grep 8000` |

4. **数据目录权限**（`DATA_DIR=/www/liubai` 时）：

```bash
# 推荐：一键设置（clay 可部署，www-data 可写上传/数据库）
sudo DEPLOY_USER=clay ./scripts/set-permissions.sh
```

脚本会：
- 项目代码归部署用户（`clay`），`.env` 为 `600`，可直接编辑
- `uploads/`、数据库归 `www-data`，目录 `775`、库文件 `664`
- 将部署用户加入 `www-data` 组

手动设置（等价逻辑）：

```bash
sudo mkdir -p /www/liubai/uploads
sudo chown -R clay:clay /www/liubai
sudo find /www/liubai -type d -exec chmod 755 {} +
sudo find /www/liubai -type f -exec chmod 644 {} +
sudo chmod 600 /www/liubai/backend/.env
sudo chown -R www-data:www-data /www/liubai/uploads
sudo chmod 775 /www/liubai/uploads
sudo chown www-data:www-data /www/liubai/db.sqlite3 2>/dev/null || true
sudo usermod -aG www-data clay
# 重新登录 SSH 后 id 应含 www-data
```

5. **启用并重启**：

```bash
sudo cp deploy/liubai.service /etc/systemd/system/liubai.service
sudo systemctl daemon-reload
sudo systemctl enable liubai
sudo systemctl restart liubai
sudo systemctl status liubai
```

更新：在 `/www/liubai` 拉代码后重新执行 `deploy-nginx.sh` 或手动 `git pull && systemctl restart liubai`。

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

见 `backend/.env.example`。Nginx 部署时 `DATA_DIR=/www/liubai`、`UPLOAD_DIR=/www/liubai/uploads`（Nginx `location ^~ /uploads/` 的 `alias` 需与此一致），`SERVE_STATIC=false`。

### 上传图片 404 / 403

一键修复（统一目录、迁移旧文件、修正 Nginx）：

```bash
cd /www/liubai
git pull origin master
sudo chmod +x scripts/fix-production-uploads.sh
sudo DEPLOY_USER=clay ./scripts/fix-production-uploads.sh
cd frontend && npm run build
```

手动排查要点：

1. **Nginx 正则抢匹配**：

```nginx
location ^~ /uploads/ {
    alias /www/liubai/uploads/;
}
```

2. **路径不一致**：后端实际写入目录须与 Nginx `alias` 相同。在服务器上核对：

```bash
grep -E 'DATA_DIR|UPLOAD_DIR' /www/liubai/backend/.env
find /www/liubai -name 'a73ba999af1944daa7bf507974645e31.jpg'
```

若文件在 `backend/uploads/` 而 Nginx 指向 `/www/liubai/uploads/`，要么改 `.env` 并迁移文件，要么改 Nginx `alias` 为 `/www/liubai/backend/uploads/`。

## 上线检查

- [ ] `SECRET_KEY`、`ADMIN_PASSWORD` 已修改
- [ ] Nginx 域名与路径正确
- [ ] `systemctl status blog` 为 active
- [ ] 首页、登录、上传正常
