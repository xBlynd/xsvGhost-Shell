#!/usr/bin/env bash
# Linux launcher for Ghost Shell (Phoenix rebuild)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONUNBUFFERED=1

# 1) Prefer host python3 if available
if command -v python3 >/dev/null 2>&1; then
  cd "$SCRIPT_DIR/src" || exit 1
  exec python3 main.py
fi

# 2) Fallback to portable Python in bin/python/python3
if [ -x "$SCRIPT_DIR/bin/python/python3" ]; then
  cd "$SCRIPT_DIR/src" || exit 1
  exec "$SCRIPT_DIR/bin/python/python3" main.py
fi

echo "[!] No python3 on host and no portable runtime in bin/python."
exit 1
