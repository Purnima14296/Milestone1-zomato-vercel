# Phase 7 — FastAPI

Run from the **repository root** with the virtualenv activated and `pip install -e ".[api]"`.

**Production (Render)**: see [DEPLOYMENT.md](../DEPLOYMENT.md) at the repo root.

```bash
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

- Docs: http://127.0.0.1:8000/docs  
- Requires `data/processed/restaurants.parquet` (Phase 1) and `GROQ_API_KEY` in the repo root `.env`.

Environment:

| Variable | Purpose |
|----------|---------|
| `API_CORS_ORIGINS` | Comma-separated origins for CORS (default `http://localhost:3000`) |
| `API_CORS_DISABLE_LOCALHOST_REGEX` | Set `1` in production; auto-set on Render if unset |
| `ZOMATO_PROCESSED_DATASET` | Parquet path (e.g. `/var/data/restaurants.parquet` on Render disk) |
| `ZOMATO_AUTO_INGEST_IF_MISSING` | Set `1` to run Phase 1 ingest on startup when Parquet is absent |
| `RENDER_SKIP_DATASET_INGEST` | Set `1` with persistent disk (see `render.disk.yaml`) |
| `GROQ_API_KEY` / `GROQ_MODEL` | Loaded via `zomato_rec.config.Settings` from env / `.env` |

**Render**: use `bash scripts/render_build.sh` as build command and `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT` as start command. Health: `GET /api/health`.
