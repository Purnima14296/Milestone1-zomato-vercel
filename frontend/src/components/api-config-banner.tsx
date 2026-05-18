"use client";

import { apiConfigurationHint, isVercel } from "@/lib/env";

export function ApiConfigBanner() {
  return (
    <div
      className="rounded-lg border border-amber-500/50 bg-amber-500/10 px-4 py-3 text-sm text-amber-100"
      role="alert"
    >
      <p className="font-semibold text-amber-200">API URL not configured</p>
      <p className="mt-1 text-amber-100/90">{apiConfigurationHint()}</p>
      {isVercel() ? (
        <p className="mt-2 text-xs text-amber-200/80">
          Example:{" "}
          <code className="rounded bg-zomato-dark px-1.5 py-0.5">
            NEXT_PUBLIC_API_URL=https://your-app.onrender.com
          </code>
        </p>
      ) : null}
    </div>
  );
}
