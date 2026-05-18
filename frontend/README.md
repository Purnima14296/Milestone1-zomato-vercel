# Phase 8 — Next.js frontend

## Local setup

```bash
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000 . The UI calls the Phase 7 API; set `NEXT_PUBLIC_API_URL` in `.env.local` if the backend is not at `http://127.0.0.1:8000`.

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
| **Build command** | `npm run build` (default; also in `vercel.json`) |

### Environment variables

| Key | Environments | Value |
|-----|----------------|--------|
| `NEXT_PUBLIC_API_URL` | Production, Preview | `https://<your-render-service>.onrender.com` (no trailing slash) |

Copy from `.env.example` or `.env.local.example`. The build **fails on Vercel** if `NEXT_PUBLIC_API_URL` is missing.

After deploy, set Render `API_CORS_ORIGINS` to your Vercel URL (e.g. `https://your-app.vercel.app`) and redeploy Render.

### Files

| File | Purpose |
|------|---------|
| `vercel.json` | Install/build commands for Vercel |
| `next.config.mjs` | Validates `NEXT_PUBLIC_API_URL` on Vercel builds |
| `src/lib/env.ts` | Resolves API base URL |
| `src/lib/api.ts` | Fetch helpers + CORS-friendly errors |
