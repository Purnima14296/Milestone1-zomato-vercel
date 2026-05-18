/**
 * Public API base URL (Render in production, local uvicorn in dev).
 * Set `NEXT_PUBLIC_API_URL` in Vercel → Environment Variables — see DEPLOYMENT.md.
 */
export function getApiBaseUrl(): string {
  const raw = process.env.NEXT_PUBLIC_API_URL?.trim();
  if (raw) return raw.replace(/\/$/, "");
  if (process.env.NODE_ENV === "production") return "";
  return "http://127.0.0.1:8000";
}

export function isApiConfigured(): boolean {
  return getApiBaseUrl().length > 0;
}

export function isVercel(): boolean {
  return process.env.VERCEL === "1";
}

export function isProductionBuild(): boolean {
  return process.env.NODE_ENV === "production";
}

/** Shown when `NEXT_PUBLIC_API_URL` is missing on Vercel/production builds. */
export function apiConfigurationHint(): string {
  if (isVercel()) {
    return "In Vercel → Project → Settings → Environment Variables, set NEXT_PUBLIC_API_URL to your Render API URL (no trailing slash), then redeploy.";
  }
  return "Set NEXT_PUBLIC_API_URL in frontend/.env.local (local) or Vercel environment variables (production). See DEPLOYMENT.md.";
}
