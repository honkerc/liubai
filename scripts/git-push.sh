#!/usr/bin/env bash
# 留白 — 经代理推送（Linux / macOS，或 Windows Git Bash）
# 用法: ./scripts/git-push.sh [remote] [branch]
set -euo pipefail

PROXY="${GIT_PUSH_PROXY:-http://127.0.0.1:7890}"
REMOTE="${1:-origin}"
BRANCH="${2:-$(git rev-parse --abbrev-ref HEAD)}"

export HTTP_PROXY="$PROXY"
export HTTPS_PROXY="$PROXY"
export ALL_PROXY="$PROXY"

echo ">> git push $REMOTE $BRANCH (proxy $PROXY)"

git -c http.sslBackend=openssl \
    -c http.proxy="$PROXY" \
    -c https.proxy="$PROXY" \
    -c http.version=HTTP/1.1 \
    push "$REMOTE" "$BRANCH"

echo "推送成功。"
