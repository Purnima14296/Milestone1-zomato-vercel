# Phase 8 — Next.js frontend

## Local setup

```bash
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000 . Set `NEXT_PUBLIC_API_URL` in `.env.local` if the backend is not at `http://127.0.0.1:8000`.

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Development server on port 3000 |
| `npm run build` | Production build |
| `npm run start` | Run production build |

No Groq or other secrets belong in this app — only the public API base URL.

## Production (Vercel)

Full checklist: **`../DEPLOYMENT.md`** §2.

| Vercel setting | Value |
|----------------|--------|
| **Root directory** | `frontend` |
| **Framework** | Next.js |

### Environment variables

| Key | Environments | Value |
|-----|----------------|--------|
| `NEXT_PUBLIC_API_URL` | Production, Preview | `https://<your-railway-domain>.up.railway.app` (no trailing slash) |

After deploy, set Railway `API_CORS_ORIGINS` to your Vercel URL if needed (`API_CORS_ALLOW_VERCEL_REGEX=1` is on by default on Railway).

### Files

| File | Purpose |
|------|---------|
| `vercel.json` | Install/build commands for Vercel |
| `next.config.mjs` | Validates `NEXT_PUBLIC_API_URL` on Vercel builds |
| `src/lib/env.ts` | Resolves API base URL |
| `src/lib/api.ts` | Fetch helpers + production error messages |
