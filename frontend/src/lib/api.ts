import type { LocationsResponse, RecommendationRequest, RecommendationResponse } from "@/lib/types";
import { getApiBaseUrl, isApiConfigured } from "@/lib/env";

export { getApiBaseUrl, isApiConfigured };

async function parseError(res: Response): Promise<string> {
  try {
    const data = (await res.json()) as { detail?: unknown };
    const d = data.detail;
    if (typeof d === "string") return d;
    if (Array.isArray(d)) {
      const parts = d
        .map((x) => {
          if (x && typeof x === "object" && "msg" in x) return String((x as { msg: unknown }).msg);
          return JSON.stringify(x);
        })
        .filter(Boolean);
      if (parts.length) return parts.join("; ");
    }
  } catch {
    /* ignore */
  }
  return await res.text().catch(() => res.statusText);
}

export function formatApiError(err: unknown): string {
  if (!isApiConfigured()) {
    return "API URL is not configured. Set NEXT_PUBLIC_API_URL in Vercel to your Render service URL.";
  }
  if (err instanceof TypeError) {
    return (
      "Cannot reach the API. Check NEXT_PUBLIC_API_URL on Vercel and API_CORS_ORIGINS on Render " +
      `(must include this site’s origin). API: ${getApiBaseUrl()}`
    );
  }
  if (err instanceof Error) return err.message;
  return "Something went wrong.";
}

async function apiFetch(path: string, init?: RequestInit): Promise<Response> {
  if (!isApiConfigured()) {
    throw new Error(formatApiError(null));
  }
  const url = `${getApiBaseUrl()}${path}`;
  try {
    return await fetch(url, init);
  } catch (err) {
    throw new Error(formatApiError(err));
  }
}

export async function getLocations(): Promise<LocationsResponse> {
  const res = await apiFetch("/api/locations", { cache: "no-store" });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json() as Promise<LocationsResponse>;
}

export async function postRecommendations(
  body: RecommendationRequest,
): Promise<RecommendationResponse> {
  const res = await apiFetch("/api/recommendations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(await parseError(res));
  }
  return res.json() as Promise<RecommendationResponse>;
}

export async function getHealth(): Promise<Record<string, unknown>> {
  const res = await apiFetch("/api/health", { cache: "no-store" });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json() as Promise<Record<string, unknown>>;
}
