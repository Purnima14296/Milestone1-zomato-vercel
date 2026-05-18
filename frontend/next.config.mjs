/** @type {import('next').NextConfig} */

const apiUrl = process.env.NEXT_PUBLIC_API_URL?.trim().replace(/\/$/, "") || "";

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    if (!apiUrl) return [];
    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

if (process.env.VERCEL === "1" && !apiUrl) {
  console.warn(
    "\n[Vercel] NEXT_PUBLIC_API_URL is not set. Add it under Project → Settings → Environment Variables, then redeploy.\n",
  );
}

export default nextConfig;
