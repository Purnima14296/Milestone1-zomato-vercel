import { apiConfigurationHint, getApiBaseUrl, isVercel } from "@/lib/env";
import type { LocationsResponse, RecommendationRequest, RecommendationResponse } from "@/lib/types";

export class ApiConfigurationError extends Error {
  constructor(message?: string) {
    super(message ?? apiConfigurationHint());
    this.name = "ApiConfigurationError";
  }
}

function requireApiBase(): string {
  const base = getApiBaseUrl();
  if (!base) throw new ApiConfigurationError();
  return base;
}

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

function wrapFetchError(err: unknown): Error {
  if (err instanceof ApiConfigurationError) return err;
  if (err instanceof TypeError) {
    const msg = String(err.message).toLowerCase();
    if (msg.includes("fetch") || msg.includes("network") || msg.includes("failed")) {
      if (isVercel()) {
        return new Error(
          "Cannot reach the API. Confirm NEXT_PUBLIC_API_URL points to your Render service and API_CORS_ORIGINS on Render includes this Vercel URL.",
        );
      }
      return new Error(
        "Cannot reach the API. Start the backend: python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000",
      );
    }
  }
  return err instanceof Error ? err : new Error(String(err));
}

async function apiFetch(path: string, init?: RequestInit): Promise<Response> {
  const base = requireApiBase();
  try {
    return await fetch(`${base}${path}`, init);
  } catch (e) {
    throw wrapFetchError(e);
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
  if (!res.ok) throw new Error(await parseError(res));
  return res.json() as Promise<RecommendationResponse>;
}

export async function getHealth(): Promise<Record<string, unknown>> {
  const res = await apiFetch("/api/health", { cache: "no-store" });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json() as Promise<Record<string, unknown>>;
}
