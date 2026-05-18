/** @type {import('next').NextConfig} */
const isVercel = process.env.VERCEL === "1";
const apiUrl = process.env.NEXT_PUBLIC_API_URL?.trim();

if (isVercel && !apiUrl) {
  throw new Error(
    "Missing NEXT_PUBLIC_API_URL. In Vercel → Project → Settings → Environment Variables, " +
      "set NEXT_PUBLIC_API_URL to your Railway API URL (e.g. https://your-app.up.railway.app). " +
      "See DEPLOYMENT.md §2.2.",
  );
}

const nextConfig = {
  reactStrictMode: true,
};

export default nextConfig;
