# Deployment plan — Railway (backend) + Vercel (frontend)

| Service | Platform | Code | Public URL (example) |
|---------|----------|------|----------------------|
| **API** (FastAPI) | [Railway](https://railway.app) | Repo root | `https://zomato-api.up.railway.app` |
| **Web** (Next.js) | [Vercel](https://vercel.com) | `frontend/` | `https://your-app.vercel.app` |

GitHub: [Milestone1-zomato-vercel](https://github.com/Purnima14296/Milestone1-zomato-vercel).

---

## Architecture

```text
User browser
    │
    ▼ HTTPS
Vercel (Next.js, NEXT_PUBLIC_API_URL)
    │
    ▼  same-origin /api/* (rewritten server-side) OR direct HTTPS to Railway
Railway (uvicorn → FastAPI)
    │
    ├── restaurants.parquet  (volume or build output)
    └── Groq API             (GROQ_API_KEY, server-side only)
```

**Secrets:** `GROQ_API_KEY` only on Railway. Vercel gets `NEXT_PUBLIC_API_URL` (public).

---

## Part 1 — Backend on Railway

### 1.1 Create the service

1. [Railway](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
2. Select **Milestone1-zomato-vercel**.
3. **Root directory:** repository root (not `frontend/`).
4. Railway reads `railway.toml` and **`Dockerfile`** (recommended — `python:3.12-slim` includes pip).

| Setting | Value |
|---------|--------|
| **Builder** | `DOCKERFILE` (see `railway.toml`) |
| **Build** | `docker build` using root `Dockerfile` — `python -m pip install ".[api]"` |
| **Start** | `scripts/railway_start.sh` → uvicorn on `0.0.0.0:$PORT` (do **not** set a custom start command in Railway UI) |
| **Health check** | `/api/health` |

After deploy, open `https://<your-service>.up.railway.app/api/health` (API only — UI is on Vercel). Root `/` redirects to `/api/health`.

Fallback: Nixpacks (`nixpacks.toml` with `providers = ["python"]`) — do **not** use `ensurepip` on Railway/Nix.

### 1.2 Environment variables (Railway)

| Key | Required | Notes |
|-----|----------|--------|
| `GROQ_API_KEY` | Yes | Groq secret |
| `GROQ_MODEL` | No | Default `llama-3.3-70b-versatile` |
| `API_CORS_ORIGINS` | Recommended | `https://your-app.vercel.app` (exact origin) |
| `API_CORS_ALLOW_VERCEL` | No | `1` (default) — allows `https://*.vercel.app` |
| `API_CORS_DISABLE_LOCALHOST_REGEX` | No | Auto-set to `1` on Railway |
| `ZOMATO_PROCESSED_DATASET` | With volume | `/data/processed/restaurants.parquet` |
| `ZOMATO_AUTO_INGEST_IF_MISSING` | No (avoid on Railway) | Dataset is baked at **Docker build**; runtime ingest can OOM. Use `1` only with a `/data` volume. |
| `HF_TOKEN` | Optional | Hugging Face token for faster dataset download at build time |
| `RAILWAY_SKIP_DATASET_INGEST` | Option C + volume | `1` — skip ingest in `scripts/railway_build.sh` |
| `HF_DATASET_ID` / `HF_DATASET_SPLIT` | No | For ingest |
| `LOG_LEVEL` | No | `INFO` |

Generate a **public domain** in Railway → **Settings** → **Networking**.

### 1.3 Dataset (required)

API returns **503** without `restaurants.parquet`.

**Option A — Railway volume (recommended)**

1. Add a **Volume**, mount at `/data`.
2. One-time in Railway **Shell**:
   ```bash
   python3 -m pip install -r requirements.txt
   python3 -m pip install ".[api]"
   python3 -m zomato_rec.phase1.ingest --out /data/processed/restaurants.parquet
   ```
3. Set `ZOMATO_PROCESSED_DATASET=/data/processed/restaurants.parquet`.

**Option B — Startup ingest**

Set `ZOMATO_AUTO_INGEST_IF_MISSING=1` (first boot ~1–4 min from Hugging Face).

**Option C — Build-time ingest**

Set Railway **build command** to:

```bash
bash scripts/railway_build.sh
```

Runs `python3 -m pip install` and Phase 1 ingest into `data/processed/` (ephemeral unless you use a volume). Skip ingest when a volume is used: set `RAILWAY_SKIP_DATASET_INGEST=1` and `ZOMATO_PROCESSED_DATASET=/data/processed/restaurants.parquet`.

### 1.4 Verify Railway

`GET https://<your-service>.up.railway.app/api/health`

Expect:

```json
{
  "status": "ok",
  "dataset_ok": true,
  "groq_configured": true,
  "railway": true,
  "cors_production_origin_configured": true
}
```

Docs: `/docs`

---

## Part 2 — Frontend on Vercel

### 2.1 Import project

| Setting | Value |
|---------|--------|
| **Root directory** | `frontend` |
| **Framework** | Next.js |

Or use repo-root `vercel.json` (builds `frontend/` automatically).

### 2.2 Environment variables (Vercel)

| Key | Environments | Value |
|-----|----------------|-------|
| `NEXT_PUBLIC_API_URL` | Production, Preview | `https://<your-railway-service>.up.railway.app` (no trailing slash) |
| `API_URL` | Production, Preview | Same as `NEXT_PUBLIC_API_URL` (server proxy fallback) |

- No trailing slash.
- **Redeploy after changing** — baked in at build time.
- Vercel **route proxy** `frontend/src/app/api/[...path]/route.ts` forwards `/api/*` → Railway (`maxDuration` 60s).
- Browser uses **same-origin** `/api/*` on Vercel (proxied to Railway — avoids CORS). Do not call Railway from the browser directly.

### 2.3 Verify UI

1. Open Vercel URL.
2. Locations load (`GET /api/locations`).
3. Submit preferences → recommendations work.

---

## Part 3 — Deploy checklist

- [ ] Railway service deployed with `GROQ_API_KEY`
- [ ] Dataset on volume or `ZOMATO_AUTO_INGEST_IF_MISSING=1`
- [ ] `/api/health` → `dataset_ok: true`
- [ ] Vercel `NEXT_PUBLIC_API_URL` = Railway URL
- [ ] Vercel redeployed
- [ ] End-to-end test on production

---

## Part 4 — Local development

**Backend** (repo root):

```bash
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend:**

```bash
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

`NEXT_PUBLIC_API_URL=http://127.0.0.1:8000` in `frontend/.env.local`.

---

## Part 5 — Troubleshooting

| Symptom | Fix |
|---------|-----|
| `503` / no dataset | Volume + ingest, or `ZOMATO_AUTO_INGEST_IF_MISSING=1` |
| CORS error | Set `API_CORS_ORIGINS` or keep `API_CORS_ALLOW_VERCEL=1` on Railway |
| Vercel “Cannot reach API” | Set `NEXT_PUBLIC_API_URL`, redeploy Vercel |
| Vercel **502** on `/api/recommendations` | Set `NEXT_PUBLIC_API_URL` + `API_URL` on Vercel; redeploy. Pro plan for 60s proxy `maxDuration`. Check Railway logs for Groq errors. |
| CORS blocked on `*.railway.app` | Use Vercel proxy (same-origin `/api/*`), not direct Railway URL in the browser. Redeploy frontend after env fix. |
| Railway/Vercel **502** on recommendations (~1s) | Often worker OOM reloading parquet. Redeploy backend (slim dataset cache, lazy load). Use Railway plan with **≥1 GB RAM**. Check logs for `recommendations: phase3/phase4`. |
| Railway **restart loop** at `Loading dataset cache` | Fixed: no synchronous cache warm at startup. `/api/health` starts first; cache loads on first recommendation. |
| `cors_production_origin_configured: false` | Redeploy Railway with latest code; check `API_CORS_ALLOW_VERCEL` |
| Cold start | Railway free tier may sleep; wait and retry |
| Deploy: `'$PORT' is not a valid integer` | Clear **Custom Start Command** in Railway; use Dockerfile `CMD` → `railway_start.sh` only |
| URL won’t load / connection refused | Logs must show `Railway start: binding 0.0.0.0:<PORT>` and `Uvicorn running on http://0.0.0.0:<PORT>` with the **same** `<PORT>` as Railway **Variables** → `PORT`. Enable **Public Networking** and generate a domain. |
| Crash loop during HF ingest | Dataset is **baked in the Docker image** at build time (`Dockerfile`). Remove `ZOMATO_AUTO_INGEST_IF_MISSING=1` from Railway vars. Optional: mount a volume at `/data` and set `ZOMATO_PROCESSED_DATASET=/data/processed/restaurants.parquet`. |
| Build: `ensurepip` failed | Use **Dockerfile** builder (`railway.toml`); do not use `python3 -m ensurepip` on Nix |
| Build: `pip: command not found` | Use `python -m pip` or Dockerfile (not bare `pip`) |
| Build: `No module named pip` | Switch builder to **DOCKERFILE**; clear custom build command in Railway UI |

---

## Files reference

| File | Purpose |
|------|---------|
| `Dockerfile` | **Recommended** — `python:3.12-slim`, pip included |
| `.dockerignore` | Keeps frontend/`node_modules` out of API image |
| `railway.toml` | `builder = DOCKERFILE`, start command, health check |
| `nixpacks.toml` / `Procfile` | Nixpacks fallback only |
| `requirements.txt` | Flat dependency list (reference / fallback) |
| `nixpacks.toml` | Nixpacks install phase (`python3 -m pip install ".[api]"`) |
| `scripts/railway_start.sh` | Production start — `0.0.0.0` + Railway `PORT` |
| `scripts/railway_install.sh` | Manual/local install helper (optional) |
| `runtime.txt` | Python 3.12 |
| `backend/app/railway_env.py` | Railway + Vercel CORS |
| `backend/app/dataset.py` | Dataset path + optional ingest |
| `backend/app/main.py` | FastAPI app |
| `scripts/railway_build.sh` | Optional build-time install + Phase 1 ingest |
| `frontend/src/app/api/[...path]/route.ts` | Server proxy `/api/*` → Railway |
| `frontend/vercel.json` | `maxDuration: 60` for API proxy |
| `frontend/next.config.mjs` | Next.js config (API URL warnings at build) |
| `frontend/vercel.json` | Vercel build |
| `frontend/.env.production.example` | Vercel env template |
