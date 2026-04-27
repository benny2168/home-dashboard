import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get("q") || "";
  const page = req.nextUrl.searchParams.get("page") || "1";

  if (!q) return NextResponse.json([]);

  try {
    const params = new URLSearchParams({
      q: `${q} wallpaper background`,
      page,
      page_size: "12",
      license_type: "all-cc",
      aspect_ratio: "wide",
      size: "large",
    });
    const resp = await fetch(`https://api.openverse.org/v1/images/?${params}`, {
      headers: { "User-Agent": "HomeDashboard/1.0 (church internal tool)" },
    });
    if (!resp.ok) {
      console.error("Openverse API error:", resp.status, await resp.text());
      return NextResponse.json([]);
    }
    const data = await resp.json();
    const results = (data.results || []).map((r: any) => ({
      url: r.url,
      thumb: r.thumbnail || r.url,
      title: r.title || "",
      creator: r.creator || "",
    }));
    return NextResponse.json(results);
  } catch (err) {
    console.error("Openverse search error:", err);
    return NextResponse.json([]);
  }
}
