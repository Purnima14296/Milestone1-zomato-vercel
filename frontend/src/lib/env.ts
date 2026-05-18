/**
 * Public API base URL (Railway in production via Vercel rewrite, local uvicorn in dev).
 * Set `NEXT_PUBLIC_API_URL` in Vercel → Environment Variables — see DEPLOYMENT.md.
 */

/** Inlined at build time when set in Vercel. */
export function configuredApiUrl(): string {
  return process.env.NEXT_PUBLIC_API_URL?.trim().replace(/\/$/, "") ?? "";
}

export function isLocalDev(): boolean {
  return process.env.NODE_ENV !== "production";
}

/** True when the app runs on a deployed host (Vercel), not localhost. */
export function isDeployedFrontend(): boolean {
  if (typeof window !== "undefined") {
    const h = window.location.hostname;
    return h !== "localhost" && h !== "127.0.0.1";
  }
  return process.env.NODE_ENV === "production";
}

/**
 * Base URL for fetch().
 * - Local dev: direct to uvicorn (default http://127.0.0.1:8000).
 * - Vercel production: empty string → same-origin `/api/*` (rewritten to Railway in next.config).
 */
export function getApiBaseUrl(): string {
  const configured = configuredApiUrl();
  if (isLocalDev()) {
    return configured || "http://127.0.0.1:8000";
  }
  if (configured) {
    return "";
  }
  return "";
}

export function isApiConfigured(): boolean {
  if (configuredApiUrl()) return true;
  return isLocalDev();
}

export function isVercel(): boolean {
  return isDeployedFrontend();
}

export function apiConfigurationHint(): string {
  if (isDeployedFrontend()) {
    return "In Vercel → Settings → Environment Variables, set NEXT_PUBLIC_API_URL to your Railway API URL (e.g. https://your-app.up.railway.app, no trailing slash), then redeploy.";
  }
  return "Set NEXT_PUBLIC_API_URL in frontend/.env.local for local dev. See DEPLOYMENT.md.";
}
