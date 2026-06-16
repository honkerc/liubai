#!/usr/bin/env bash
# 留白 — 设置 /www/liubai 目录权限
# 部署用户 (clay) 可 git pull、改 .env、npm build；www-data 可写上传目录与数据库
#
# 用法:
#   sudo DEPLOY_USER=clay ./scripts/set-permissions.sh
#   sudo DEPLOY_USER=clay INSTALL_ROOT=/www/liubai ./scripts/set-permissions.sh
set -euo pipefail

INSTALL_ROOT="${INSTALL_ROOT:-/www/liubai}"
DEPLOY_USER="${DEPLOY_USER:-clay}"
SERVICE_USER="${SERVICE_USER:-www-data}"
ENV_FILE="${ENV_FILE:-$INSTALL_ROOT/backend/.env}"

if [[ "$(id -u)" -ne 0 ]]; then
    echo "请使用 root 运行: sudo DEPLOY_USER=$DEPLOY_USER $0" >&2
    exit 1
fi

if [[ ! -d "$INSTALL_ROOT" ]]; then
    echo "目录不存在: $INSTALL_ROOT" >&2
    exit 1
fi

if ! id "$DEPLOY_USER" &>/dev/null; then
    echo "用户不存在: $DEPLOY_USER（可设置 DEPLOY_USER=你的用户名）" >&2
    exit 1
fi

if ! getent group "$SERVICE_USER" >/dev/null; then
    echo "组不存在: $SERVICE_USER" >&2
    exit 1
fi

# 从 backend/.env 读取 DATA_DIR / UPLOAD_DIR（若未设置则用生产默认值）
DATA_DIR="$INSTALL_ROOT"
UPLOAD_DIR="$INSTALL_ROOT/uploads"
DATABASE_NAME="db.sqlite3"
if [[ -f "$ENV_FILE" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
        line="${line%%#*}"
        line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//;s/\r$//')"
        [[ -z "$line" || "$line" != *=* ]] && continue
        key="${line%%=*}"
        val="${line#*=}"
        val="${val#\"}"; val="${val%\"}"
        val="${val#\'}"; val="${val%\'}"
        case "$key" in
            DATA_DIR) [[ -n "$val" ]] && DATA_DIR="$val" ;;
            UPLOAD_DIR) [[ -n "$val" ]] && UPLOAD_DIR="$val" ;;
            DATABASE_NAME) [[ -n "$val" ]] && DATABASE_NAME="$val" ;;
        esac
    done < "$ENV_FILE"
fi

# 未显式配置 DATA_DIR 时，后端默认使用 backend/ 目录
if [[ -f "$ENV_FILE" ]] && ! grep -qE '^[[:space:]]*DATA_DIR=' "$ENV_FILE"; then
    DATA_DIR="$INSTALL_ROOT/backend"
    if [[ "$UPLOAD_DIR" == "$INSTALL_ROOT/uploads" ]]; then
        UPLOAD_DIR="$INSTALL_ROOT/backend/uploads"
    fi
fi

DB_PATH="$DATA_DIR/$DATABASE_NAME"

echo "==> 部署用户: $DEPLOY_USER"
echo "==> 运行用户: $SERVICE_USER"
echo "==> 项目目录: $INSTALL_ROOT"
echo "==> 数据目录: $DATA_DIR"
echo "==> 上传目录: $UPLOAD_DIR"
echo "==> 数据库:   $DB_PATH"

echo "==> [1/4] 将 $DEPLOY_USER 加入 $SERVICE_USER 组"
usermod -aG "$SERVICE_USER" "$DEPLOY_USER"

echo "==> [2/4] 项目代码归 $DEPLOY_USER（可读可改，便于部署）"
chown -R "$DEPLOY_USER:$DEPLOY_USER" "$INSTALL_ROOT"
find "$INSTALL_ROOT" -type d -exec chmod 755 {} +
find "$INSTALL_ROOT" -type f -exec chmod 644 {} +
if [[ -f "$ENV_FILE" ]]; then
    chown "$DEPLOY_USER:$DEPLOY_USER" "$ENV_FILE"
    chmod 600 "$ENV_FILE"
fi
if [[ -d "$INSTALL_ROOT/.venv" ]]; then
    chmod -R o+rX "$INSTALL_ROOT/.venv"
fi

echo "==> [3/4] 运行时目录归 $SERVICE_USER（上传、数据库）"
mkdir -p "$UPLOAD_DIR" "$(dirname "$DB_PATH")"

chown -R "$SERVICE_USER:$SERVICE_USER" "$UPLOAD_DIR"
find "$UPLOAD_DIR" -type d -exec chmod 775 {} +
find "$UPLOAD_DIR" -type f -exec chmod 664 {} + 2>/dev/null || true
chmod 775 "$UPLOAD_DIR"

# 兼容旧布局：backend/uploads、backend/db.sqlite3
LEGACY_UPLOAD="$INSTALL_ROOT/backend/uploads"
LEGACY_DB="$INSTALL_ROOT/backend/$DATABASE_NAME"
if [[ "$LEGACY_UPLOAD" != "$UPLOAD_DIR" && -d "$LEGACY_UPLOAD" ]]; then
    chown -R "$SERVICE_USER:$SERVICE_USER" "$LEGACY_UPLOAD"
    find "$LEGACY_UPLOAD" -type d -exec chmod 775 {} +
    find "$LEGACY_UPLOAD" -type f -exec chmod 664 {} + 2>/dev/null || true
fi
if [[ "$LEGACY_DB" != "$DB_PATH" && -f "$LEGACY_DB" ]]; then
    chown "$SERVICE_USER:$SERVICE_USER" "$LEGACY_DB" "${LEGACY_DB}"-* 2>/dev/null || true
    chmod 664 "$LEGACY_DB" 2>/dev/null || true
    chmod 664 "${LEGACY_DB}"-* 2>/dev/null || true
fi

if [[ -f "$DB_PATH" ]]; then
    chown "$SERVICE_USER:$SERVICE_USER" "$DB_PATH"
    chmod 664 "$DB_PATH"
fi
for extra in "$DB_PATH-wal" "$DB_PATH-shm" "$DB_PATH-journal"; do
    if [[ -f "$extra" ]]; then
        chown "$SERVICE_USER:$SERVICE_USER" "$extra"
        chmod 664 "$extra"
    fi
done
if [[ -d "$DATA_DIR" && "$DATA_DIR" != "$INSTALL_ROOT" ]]; then
    chown "$SERVICE_USER:$SERVICE_USER" "$DATA_DIR" 2>/dev/null || true
    chmod 775 "$DATA_DIR" 2>/dev/null || true
fi

echo "==> [4/4] 完成"
echo ""
echo "权限已设置。请 $DEPLOY_USER 重新登录 SSH（或执行: newgrp $SERVICE_USER）后生效。"
echo "验证:"
echo "  id $DEPLOY_USER"
echo "  ls -la $ENV_FILE"
echo "  ls -ld $UPLOAD_DIR"
echo "  sudo -u $SERVICE_USER touch $UPLOAD_DIR/.perm-test && sudo rm $UPLOAD_DIR/.perm-test"
