#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-4321}"
DOC_PATH="${DOC_PATH:-/docs/learning-roadmap}"
URL="http://${HOST}:${PORT}${DOC_PATH}"

cd "$ROOT_DIR"

if ! command -v pnpm >/dev/null 2>&1; then
  echo "pnpm 未安装。请先安装 pnpm 后再运行这个脚本。"
  exit 1
fi

if [ ! -d node_modules ]; then
  echo "正在安装依赖..."
  pnpm install
fi

echo "启动本地站点：$URL"

if command -v open >/dev/null 2>&1; then
  (
    sleep 2
    open "$URL" >/dev/null 2>&1 || true
  ) &
fi

exec pnpm dev --host "$HOST" --port "$PORT"
