#!/usr/bin/env bash
# 生产环境更新：务必先 pull，再构建前端，最后重启 API
set -euo pipefail

INSTALL_ROOT="${INSTALL_ROOT:-/www/liubai}"
DEPLOY_USER="${DEPLOY_USER:-clay}"

if [[ "$(id -un)" != "$DEPLOY_USER" && "$(id -un)" != "root" ]]; then
    echo "请使用 $DEPLOY_USER 或 root 运行" >&2
    exit 1
fi

cd "$INSTALL_ROOT"

echo "==> git pull origin master"
git pull origin master

echo "==> npm ci && npm run build (frontend)"
cd frontend
npm ci
npm run build

echo "==> restart liubai"
if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl restart liubai
    sudo systemctl status liubai --no-pager || true
else
    echo "未找到 systemctl，请手动重启 API" >&2
fi

echo "==> 完成"
