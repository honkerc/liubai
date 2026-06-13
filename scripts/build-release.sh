#!/usr/bin/env bash
# 构建前端生产包（供 Nginx 托管）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND="$ROOT/frontend"
DIST="$FRONTEND/dist"

echo "==> 构建前端"
cd "$FRONTEND"
if [[ -f package-lock.json ]]; then
    npm ci --no-audit --no-fund
else
    npm install --no-audit --no-fund
fi
npm run build

if [[ ! -f "$DIST/index.html" ]]; then
    echo "错误: 未找到 $DIST/index.html" >&2
    exit 1
fi

echo "==> 完成: $DIST"
