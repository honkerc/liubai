#!/usr/bin/env bash
# 留白 — 统一生产环境上传目录，并修正 Nginx /uploads 配置
#
# 解决：文件在 backend/uploads、Nginx alias 指错、location ~ 导致 404/403
#
# 用法:
#   sudo ./scripts/fix-production-uploads.sh
#   sudo NGINX_SITE=/etc/nginx/sites-available/honkerc.cn ./scripts/fix-production-uploads.sh
set -euo pipefail

INSTALL_ROOT="${INSTALL_ROOT:-/www/liubai}"
ENV_FILE="${ENV_FILE:-$INSTALL_ROOT/backend/.env}"
NGINX_SITE="${NGINX_SITE:-/etc/nginx/sites-available/honkerc.cn}"
SERVICE_USER="${SERVICE_USER:-www-data}"
DEPLOY_USER="${DEPLOY_USER:-clay}"

DATA_DIR="$INSTALL_ROOT"
UPLOAD_DIR="$INSTALL_ROOT/uploads"
LEGACY_UPLOAD="$INSTALL_ROOT/backend/uploads"

if [[ "$(id -u)" -ne 0 ]]; then
    echo "请使用 root 运行: sudo $0" >&2
    exit 1
fi

if [[ ! -d "$INSTALL_ROOT" ]]; then
    echo "目录不存在: $INSTALL_ROOT" >&2
    exit 1
fi

echo "==> [1/5] 写入 backend/.env（DATA_DIR / UPLOAD_DIR）"
mkdir -p "$(dirname "$ENV_FILE")"
if [[ ! -f "$ENV_FILE" ]]; then
    cp "$INSTALL_ROOT/backend/.env.example" "$ENV_FILE"
fi

touch "$ENV_FILE"
grep -q '^DATA_DIR=' "$ENV_FILE" \
    && sed -i "s|^DATA_DIR=.*|DATA_DIR=$DATA_DIR|" "$ENV_FILE" \
    || echo "DATA_DIR=$DATA_DIR" >> "$ENV_FILE"
grep -q '^UPLOAD_DIR=' "$ENV_FILE" \
    && sed -i "s|^UPLOAD_DIR=.*|UPLOAD_DIR=$UPLOAD_DIR|" "$ENV_FILE" \
    || echo "UPLOAD_DIR=$UPLOAD_DIR" >> "$ENV_FILE"

echo "==> [2/5] 迁移 backend/uploads → $UPLOAD_DIR（若存在旧数据）"
mkdir -p "$UPLOAD_DIR"
if [[ -d "$LEGACY_UPLOAD" ]] && [[ -n "$(ls -A "$LEGACY_UPLOAD" 2>/dev/null || true)" ]]; then
    cp -a "$LEGACY_UPLOAD/." "$UPLOAD_DIR/"
    echo "    已从 $LEGACY_UPLOAD 合并文件"
fi

echo "==> [3/5] 目录权限"
chown -R "$SERVICE_USER:$SERVICE_USER" "$UPLOAD_DIR"
find "$UPLOAD_DIR" -type d -exec chmod 775 {} +
find "$UPLOAD_DIR" -type f -exec chmod 664 {} + 2>/dev/null || true
chmod 755 "$INSTALL_ROOT" "$DATA_DIR" 2>/dev/null || true

if id "$DEPLOY_USER" &>/dev/null; then
    usermod -aG "$SERVICE_USER" "$DEPLOY_USER" 2>/dev/null || true
    chown -R "$DEPLOY_USER:$DEPLOY_USER" "$INSTALL_ROOT"
    find "$INSTALL_ROOT" -type d -exec chmod 755 {} +
    find "$INSTALL_ROOT" -type f -exec chmod 644 {} +
    chown "$DEPLOY_USER:$DEPLOY_USER" "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    chown -R "$SERVICE_USER:$SERVICE_USER" "$UPLOAD_DIR"
fi

echo "==> [4/5] 更新 Nginx: $NGINX_SITE"
if [[ ! -f "$NGINX_SITE" ]]; then
    echo "    未找到 $NGINX_SITE，跳过（可手动 cp deploy/honkerc.cn.conf）" >&2
else
    cp "$NGINX_SITE" "${NGINX_SITE}.bak.$(date +%Y%m%d%H%M%S)"

    # location ^~ /uploads/ + 正确 alias
    if grep -q 'location.*uploads' "$NGINX_SITE"; then
        sed -i 's|location ~ /uploads/|location ^~ /uploads/|g' "$NGINX_SITE"
        sed -i 's|location /uploads/|location ^~ /uploads/|g' "$NGINX_SITE"
        sed -i "s|alias /www/uploads/;|alias $UPLOAD_DIR/;|g" "$NGINX_SITE"
        sed -i "s|alias /www/liubai/backend/uploads/;|alias $UPLOAD_DIR/;|g" "$NGINX_SITE"
        sed -i "s|alias /www/liubai/uploads/;|alias $UPLOAD_DIR/;|g" "$NGINX_SITE"
    fi

    # 补 trailing-slash 重定向（若尚未有）
    if ! grep -q 'uploads/.+\.(webp' "$NGINX_SITE"; then
        sed -i "/client_max_body_size/a\\
\\
    rewrite ^(/uploads/.+\\.(webp|jpe?g|png|gif|svg|ico|bmp|mp4|webm|mp3|wav|pdf|zip|tar|gz|bz2|7z|rar|md|txt))/\$ \$1 permanent;" "$NGINX_SITE"
    fi

    nginx -t
    systemctl reload nginx
    echo "    Nginx 已 reload"
fi

echo "==> [5/5] 重启 API"
systemctl restart liubai 2>/dev/null || systemctl restart blog 2>/dev/null || true

echo ""
echo "完成。上传目录: $UPLOAD_DIR"
echo "验证:"
echo "  curl -I http://127.0.0.1:8000/api/health"
echo "  ls -la $UPLOAD_DIR/images/compressed/ | head"
echo "  curl -I 'https://honkerc.cn/uploads/images/compressed/某文件.webp'"
