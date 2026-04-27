import { prisma } from "@/lib/prisma";
import { auth } from "@/auth";
import { redirect } from "next/navigation";
import TabsClient from "./TabsClient";
import { Suspense } from "react";

export const dynamic = "force-dynamic";

export default async function TabsAdminPage() {
  const session = await auth();
  if (!session?.user?.isAdmin) redirect("/");

  const [tabs, users, themes] = await Promise.all([
    prisma.tab.findMany({
      orderBy: { order: "asc" },
      include: { 
        allowedUsers: { select: { id: true, name: true, email: true } },
        editors: { select: { id: true, name: true, email: true } },
        owners: { select: { id: true, name: true, email: true } },
        blockedUsers: { select: { id: true, name: true, email: true } },
        theme: true,
        departmentAccess: true
      }
    }),
    prisma.user.findMany({
        select: { id: true, name: true, email: true, department: true, isAdmin: true, avatarColor: true }
    }),
    prisma.theme.findMany()
  ]);

  // Group users by department for easier selection
  const departments = Array.from(new Set(users.map(u => u.department || "General")));

  return (
    <div className="fade-in">
       <div style={{ marginBottom: '2.5rem' }}>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, marginBottom: '0.5rem' }}>Workspace Hub</h2>
          <p style={{ opacity: 0.6 }}>Design and govern your primary dashboard workspaces.</p>
       </div>
       
       <Suspense fallback={null}>
       <TabsClient 
          initialTabs={JSON.parse(JSON.stringify(tabs))}
          users={JSON.parse(JSON.stringify(users))}
          departments={departments}
          themes={JSON.parse(JSON.stringify(themes))}
       />
       </Suspense>
    </div>
  );
}
