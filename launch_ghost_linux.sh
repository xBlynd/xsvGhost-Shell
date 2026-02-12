#!/usr/bin/env bash
# Linux launcher for Ghost Shell (Phoenix rebuild)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONUNBUFFERED=1

cd "$SCRIPT_DIR/src" || exit 1
python3 main.py
