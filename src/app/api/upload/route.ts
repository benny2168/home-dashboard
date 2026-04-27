import { NextRequest, NextResponse } from "next/server";
import { writeFile, mkdir } from "fs/promises";
import { join } from "path";

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get("file") as File;
    if (!file) return NextResponse.json({ error: "No file provided" }, { status: 400 });

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    const uploadDir = join(process.cwd(), "public", "uploads");
    await mkdir(uploadDir, { recursive: true });
    
    const filename = `${Date.now()}-${file.name.replace(/\s+/g, "-")}`;
    const path = join(uploadDir, filename);
    await writeFile(path, buffer);
    
    return NextResponse.json({ url: `/api/uploads/${filename}` });
  } catch (err: any) {
    console.error("API Upload Error:", err);
    return NextResponse.json({ error: err.message || "Manifestation failure" }, { status: 500 });
  }
}
