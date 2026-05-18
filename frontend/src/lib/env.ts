/**
 * Public API base URL (Railway in production, local uvicorn in dev).
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
