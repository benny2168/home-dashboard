import { prisma } from "@/lib/prisma";
import { LayoutGrid, Bookmark, Library, Settings } from "lucide-react";
import { GlobalDefaultTab } from "./GlobalDefaultTab";

export const dynamic = 'force-dynamic';

export default async function AdminPage() {
  const [tabsCount, sectionsCount, bookmarksCount, activeTheme, allTabs, globalSettings] = await Promise.all([
    prisma.tab.count(),
    prisma.section.count(),
    prisma.bookmark.count(),
    prisma.theme.findFirst({ where: { isActive: true } }),
    prisma.tab.findMany({ orderBy: { order: "asc" }, select: { id: true, title: true } }),
    (prisma as any).globalSettings.findUnique({ where: { id: "global" } }),
  ]);

  const stats = [
    { label: "Total Tabs", value: tabsCount, icon: Library, color: "#6366f1" },
    { label: "Total Sections", value: sectionsCount, icon: LayoutGrid, color: "#ec4899" },
    { label: "Total Bookmarks", value: bookmarksCount, icon: Bookmark, color: "#8b5cf6" },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(v-fill, minmax(200px, 1fr))', gap: '1.5rem' }}>
         <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
          {stats.map((stat, i) => (
            <div key={i} className="glass glass-card" style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
              <div style={{ background: `${stat.color}15`, color: stat.color, padding: '1rem', borderRadius: '12px' }}>
                <stat.icon size={24} />
              </div>
              <div>
                <p style={{ margin: 0, opacity: 0.5, fontSize: '0.9rem' }}>{stat.label}</p>
                <h3 style={{ margin: 0, fontSize: '1.5rem' }}>{stat.value}</h3>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="admin-card-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div className="glass glass-card">
          <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Settings size={20} />
            Quick Settings
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>Theme: {activeTheme?.name || "Default"}</span>
              <a href="/admin/theme" className="btn" style={{ border: '1px solid var(--glass-border)' }}>Edit</a>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>Content Management</span>
              <a href="/admin/content" className="btn" style={{ border: '1px solid var(--glass-border)' }}>Manage</a>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.5rem', borderTop: '1px solid var(--glass-border)' }}>
              <div>
                <span style={{ display: 'block', fontWeight: 600 }}>Default Workspace</span>
                <span style={{ fontSize: '0.75rem', opacity: 0.5 }}>Shown to users with no personal default set</span>
              </div>
              <GlobalDefaultTab allTabs={allTabs} currentDefaultTabId={globalSettings?.defaultTabId || null} />
            </div>
          </div>
        </div>

        <div className="glass glass-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center', gap: '1rem' }}>
          <div style={{ background: 'var(--primary)', color: 'white', padding: '1.5rem', borderRadius: '50%' }}>
            <Library size={32} />
          </div>
          <h3>System Overview</h3>
          <p style={{ opacity: 0.6 }}>The dashboard is active and running on Next.js 16. Databases are connected and healthy.</p>
        </div>
      </div>
    </div>
  );
}
