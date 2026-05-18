#!/usr/bin/env bash
# Install app + API deps on Railway (non-editable). Repo root.
set -euo pipefail
cd "$(dirname "$0")/.."

python -m pip install --upgrade pip
python -m pip install setuptools wheel
python -m pip install ".[api]"
