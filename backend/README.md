# Phase 7 — FastAPI

Run from the **repository root** with the virtualenv activated and `pip install -e ".[api]"`.

```bash
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

- Docs: http://127.0.0.1:8000/docs  
- Health: http://127.0.0.1:8000/api/health  
- Requires `data/processed/restaurants.parquet` (Phase 1) and `GROQ_API_KEY` in the repo root `.env`.

### Railway

| File | Purpose |
|------|---------|
| `railway.toml` | Build/start commands + health check |
| `scripts/railway_build.sh` | `pip install` + conditional Phase 1 ingest |

Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

On Railway, production CORS defaults apply automatically. Set `API_CORS_ORIGINS` to your Vercel URL if needed.

Full checklist: **`../DEPLOYMENT.md`**.

Environment:

| Variable | Purpose |
|----------|---------|
| `API_CORS_ORIGINS` | Comma-separated origins for CORS (default localhost dev ports) |
| `API_CORS_DISABLE_LOCALHOST_REGEX` | Set `1` in production to allow only `API_CORS_ORIGINS` |
| `API_CORS_ALLOW_VERCEL_REGEX` | Set `1` on Railway (default) to allow `*.vercel.app` |
| `ZOMATO_PROCESSED_DATASET` | Optional absolute path to `restaurants.parquet` (e.g. `/data/...` on a volume) |
| `GROQ_API_KEY` / `GROQ_MODEL` | Loaded via `zomato_rec.config.Settings` |
