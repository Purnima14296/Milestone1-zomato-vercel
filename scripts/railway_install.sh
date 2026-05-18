#!/usr/bin/env bash
# Install app + API deps on Railway (non-editable). Repo root.
set -euo pipefail
cd "$(dirname "$0")/.."

PY="python3"
if ! command -v "$PY" >/dev/null 2>&1; then
  PY="python"
fi

if ! "$PY" -m pip --version >/dev/null 2>&1; then
  echo "ERROR: pip is not available. Use the repo Dockerfile on Railway (python:3.12-slim)." >&2
  exit 1
fi

echo "==> Installing package and dependencies"
"$PY" -m pip install --upgrade pip setuptools wheel
"$PY" -m pip install ".[api]"
