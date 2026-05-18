import { NextRequest, NextResponse } from "next/server";

/** Vercel Pro: allow long Groq /api/recommendations upstream calls. */
export const maxDuration = 60;
export const runtime = "nodejs";

function upstreamBase(): string | null {
  const raw = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "";
  const trimmed = raw.trim().replace(/\/$/, "");
  return trimmed || null;
}

async function proxy(req: NextRequest, pathSegments: string[]): Promise<NextResponse> {
  const base = upstreamBase();
  if (!base) {
    return NextResponse.json(
      {
        detail:
          "Set API_URL and NEXT_PUBLIC_API_URL on Vercel to your Railway URL (no trailing slash), then redeploy.",
      },
      { status: 503 },
    );
  }

  const subpath = pathSegments.map(encodeURIComponent).join("/");
  const target = `${base}/api/${subpath}${req.nextUrl.search}`;

  const headers = new Headers();
  const contentType = req.headers.get("content-type");
  if (contentType) headers.set("content-type", contentType);

  const init: RequestInit = {
    method: req.method,
    headers,
    cache: "no-store",
  };
  if (req.method !== "GET" && req.method !== "HEAD") {
    init.body = await req.arrayBuffer();
  }

  let upstream: Response;
  try {
    upstream = await fetch(target, init);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return NextResponse.json(
      { detail: `Upstream unreachable (${base}): ${message}` },
      { status: 502 },
    );
  }

  const outHeaders = new Headers();
  const upstreamType = upstream.headers.get("content-type");
  if (upstreamType) outHeaders.set("content-type", upstreamType);

  return new NextResponse(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers: outHeaders,
  });
}

type RouteContext = { params: { path: string[] } };

export async function GET(req: NextRequest, ctx: RouteContext) {
  return proxy(req, ctx.params.path);
}

export async function POST(req: NextRequest, ctx: RouteContext) {
  return proxy(req, ctx.params.path);
}

export async function PUT(req: NextRequest, ctx: RouteContext) {
  return proxy(req, ctx.params.path);
}

export async function PATCH(req: NextRequest, ctx: RouteContext) {
  return proxy(req, ctx.params.path);
}

export async function DELETE(req: NextRequest, ctx: RouteContext) {
  return proxy(req, ctx.params.path);
}

export async function OPTIONS(req: NextRequest, ctx: RouteContext) {
  return proxy(req, ctx.params.path);
}
