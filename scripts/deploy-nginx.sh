#!/usr/bin/env bash
# 留白 — Linux 生产部署（Nginx + systemd）
# 用法: sudo DOMAIN=blog.example.com ./scripts/deploy-nginx.sh
set -euo pipefail

DOMAIN="${DOMAIN:-your-domain.com}"
INSTALL_ROOT="${INSTALL_ROOT:-/www/liubai}"
DATA_DIR="${DATA_DIR:-/www/liubai}"
UPLOAD_DIR="${UPLOAD_DIR:-/www/liubai/uploads}"
ENV_FILE="${ENV_FILE:-/etc/blog/env}"
SERVICE_USER="${SERVICE_USER:-www-data}"

if [[ "$(id -u)" -ne 0 ]]; then
    echo "请使用 root 运行: sudo $0" >&2
    exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$INSTALL_ROOT/.venv"
DIST="$INSTALL_ROOT/dist"

echo "==> [1/6] 构建前端"
bash "$ROOT/scripts/build-release.sh"

echo "==> [2/6] 同步项目到 $INSTALL_ROOT"
mkdir -p "$INSTALL_ROOT" "$DIST" "$UPLOAD_DIR" "$(dirname "$ENV_FILE")"

rsync -a --delete \
    --exclude node_modules \
    --exclude dist \
    --exclude .git \
    --exclude logs \
    --exclude data \
    --exclude 'backend/db.sqlite3' \
    --exclude 'backend/uploads' \
    "$ROOT/" "$INSTALL_ROOT/"

echo "==> [3/6] 安装 Python 依赖"
if [[ ! -d "$VENV" ]]; then
    python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r "$INSTALL_ROOT/backend/requirements.txt"

echo "==> [4/6] 发布前端静态文件"
rsync -a --delete "$ROOT/frontend/dist/" "$DIST/"

echo "==> [5/6] 配置 systemd"
if [[ ! -f "$ENV_FILE" ]]; then
    cp "$INSTALL_ROOT/deploy/env.example" "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    echo "已创建 $ENV_FILE — 请修改 SECRET_KEY 与 ADMIN_PASSWORD 后重启服务"
fi

sed "s|your-domain.com|$DOMAIN|g" "$INSTALL_ROOT/deploy/blog.service" \
    > /etc/systemd/system/blog.service

if [[ "$INSTALL_ROOT" != "/www/liubai" ]]; then
    sed -i "s|/www/liubai|$INSTALL_ROOT|g" /etc/systemd/system/blog.service
fi

systemctl daemon-reload
systemctl enable blog
systemctl restart blog

echo "==> [6/6] 配置 Nginx"
NGINX_SITE="/etc/nginx/sites-available/blog"
sed "s|your-domain.com|$DOMAIN|g" "$INSTALL_ROOT/deploy/nginx.conf" > "$NGINX_SITE"

if [[ "$INSTALL_ROOT" != "/www/liubai" ]] || [[ "$UPLOAD_DIR" != "/www/liubai/uploads" ]]; then
    sed -i "s|/www/liubai/dist|$DIST|g" "$NGINX_SITE"
    sed -i "s|/www/liubai/uploads/|$UPLOAD_DIR/|g" "$NGINX_SITE"
fi

ln -sf "$NGINX_SITE" /etc/nginx/sites-enabled/blog
nginx -t
systemctl reload nginx

chown -R "$SERVICE_USER:$SERVICE_USER" "$UPLOAD_DIR" "$DIST"
chown -R root:root "$INSTALL_ROOT"
chmod -R o+rX "$INSTALL_ROOT" "$VENV"

echo ""
echo "留白 部署完成"
echo "  站点:  http://$DOMAIN"
echo "  健康:  curl http://127.0.0.1:8000/api/health"
echo "  服务:  systemctl status blog"
echo "  日志:  journalctl -u blog -f"
