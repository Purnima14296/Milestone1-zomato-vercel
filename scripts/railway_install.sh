#!/usr/bin/env bash
# Install app + API deps on Railway (non-editable). Repo root.
set -euo pipefail
cd "$(dirname "$0")/.."

PY="python3"
if ! command -v "$PY" >/dev/null 2>&1; then
  PY="python"
fi

if ! "$PY" -m pip --version >/dev/null 2>&1; then
  echo "==> Bootstrapping pip via ensurepip"
  "$PY" -m ensurepip --upgrade
fi

echo "==> Installing package and dependencies"
"$PY" -m pip install --upgrade pip setuptools wheel
"$PY" -m pip install ".[api]"
