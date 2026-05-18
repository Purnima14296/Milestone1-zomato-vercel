#!/bin/sh
# Railway: must listen on 0.0.0.0 and the PORT env var (assigned per deployment).
set -e

PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"

echo "==> Railway start: binding ${HOST}:${PORT} (PORT=${PORT})"
exec python -m uvicorn backend.app.main:app --host "${HOST}" --port "${PORT}"
