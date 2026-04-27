import { NextRequest, NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";
import { existsSync } from "fs";

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path: pathSegments } = await params;
  const path = pathSegments.join("/");
  const filePath = join(process.cwd(), "public", "uploads", path);

  if (!existsSync(filePath)) {
    return new NextResponse("Not Found", { status: 404 });
  }

  try {
    const buffer = await readFile(filePath);
    const extension = path.split(".").pop()?.toLowerCase();
    
    let contentType = "image/png";
    if (extension === "jpg" || extension === "jpeg") contentType = "image/jpeg";
    if (extension === "svg") contentType = "image/svg+xml";
    if (extension === "gif") contentType = "image/gif";
    if (extension === "webp") contentType = "image/webp";

    return new NextResponse(buffer, {
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=31536000, immutable",
      },
    });
  } catch (error) {
    return new NextResponse("Error reading file", { status: 500 });
  }
}
