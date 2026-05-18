/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

if (process.env.VERCEL === "1" && !process.env.NEXT_PUBLIC_API_URL?.trim()) {
  console.warn(
    "\n[Vercel] NEXT_PUBLIC_API_URL is not set. Add it under Project → Settings → Environment Variables (see DEPLOYMENT.md).\n",
  );
}

export default nextConfig;
