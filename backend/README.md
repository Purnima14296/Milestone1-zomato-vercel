# Phase 7 — FastAPI

Run from the **repository root** with the virtualenv activated and `pip install -e ".[api]"`.

```bash
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

- Docs: http://127.0.0.1:8000/docs  
- Health: http://127.0.0.1:8000/api/health  
- Requires `data/processed/restaurants.parquet` (Phase 1) and `GROQ_API_KEY` in the repo root `.env`.

### Render

| File | Purpose |
|------|---------|
| `render.yaml` | Blueprint — build runs `scripts/render_build.sh` (Option A ingest) |
| `render.disk.yaml` | Blueprint with 1 GB disk at `/var/data` (Option B) |
| `runtime.txt` | Python 3.12.7 |
| `scripts/render_build.sh` | `pip install` + conditional Phase 1 ingest |

Start command (dashboard or blueprint):  
`uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

On Render, `API_CORS_DISABLE_LOCALHOST_REGEX=1` is applied automatically if unset. Set `API_CORS_ORIGINS` to your Vercel URL.

Full checklist: **`../DEPLOYMENT.md`**.

Environment:

| Variable | Purpose |
|----------|---------|
| `API_CORS_ORIGINS` | Comma-separated origins for CORS (default `http://localhost:3000`) |
| `API_CORS_DISABLE_LOCALHOST_REGEX` | Set `1` on Render to allow only `API_CORS_ORIGINS` |
| `ZOMATO_PROCESSED_DATASET` | Optional absolute path to `restaurants.parquet` on the server |
| `GROQ_API_KEY` / `GROQ_MODEL` | Loaded via `zomato_rec.config.Settings` from `.env` |
