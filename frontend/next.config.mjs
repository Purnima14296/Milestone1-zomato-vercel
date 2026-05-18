/** @type {import('next').NextConfig} */

/**
 * Railway API base (no trailing slash).
 * - NEXT_PUBLIC_API_URL: used by client + build
 * - API_URL: server-only fallback for /api/* route proxy
 */
const apiUrl =
  process.env.NEXT_PUBLIC_API_URL?.trim().replace(/\/$/, "") ||
  process.env.API_URL?.trim().replace(/\/$/, "") ||
  "";

const nextConfig = {
  reactStrictMode: true,
  // /api/* is proxied via src/app/api/[...path]/route.ts (not rewrites) for clearer 502 errors and maxDuration.
};

if (process.env.VERCEL === "1" && !apiUrl) {
  console.warn(
    "\n[Vercel] Set NEXT_PUBLIC_API_URL and API_URL to your Railway URL (e.g. https://web-production-843fc7.up.railway.app), then redeploy.\n",
  );
}

export default nextConfig;
