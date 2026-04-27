#!/usr/bin/env python3
import re
import os

def patch_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: Could not find snippet in {filepath}")
            if "rgba(0,0,0,0.92)" in old:
                content = re.sub(r'rgba\(0,\s*0,\s*0,\s*0\.92\)', 'rgba(0,0,0,0.4)', content)

    with open(filepath, 'w') as f:
        f.write(content)

# 1. globals.css (btn-primary hover)
globals_css = "src/app/globals.css"
patch_file(globals_css, [
    (
        "background: #4f46e5;\n  box-shadow: 0 0 25px var(--primary-glow);",
        "background: var(--primary);\n  filter: brightness(1.2);\n  box-shadow: 0 0 25px var(--primary-glow);"
    )
])

# 2. Modals dark mode contrast
modals = ["BookmarkModal.tsx", "SectionModal.tsx", "TabModal.tsx", "ThemeModal.tsx"]
for m in modals:
    path = f"src/components/{m}"
    if os.path.exists(path):
        patch_file(path, [("rgba(0,0,0,0.92)", "rgba(0,0,0,0.4)")])

# 3. IconPicker.tsx upload internally
icon_picker = "src/components/IconPicker.tsx"
ip_old = """  const handleDropLocal = async (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) onUpload(file);
  };"""

ip_new = """  const uploadFile = async (file: File) => {
      const fd = new FormData();
      fd.append("file", file);
      try {
          const res = await fetch("/api/upload", { method: "POST", body: fd });
          const data = await res.json();
          if (data.url) setIcon(data.url);
      } catch (e) {
          console.error(e);
      }
  };

  const handleDropLocal = async (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) await uploadFile(file);
  };"""

ip_input_old = """                      <input 
                        type="file" 
                        id="icon-upload-picker" 
                        hidden 
                        onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0])}
                      />"""

ip_input_new = """                      <input 
                        type="file" 
                        id="icon-upload-picker" 
                        hidden 
                        onChange={(e) => e.target.files?.[0] && uploadFile(e.target.files[0])}
                      />"""

patch_file(icon_picker, [(ip_old, ip_new), (ip_input_old, ip_input_new)])

# 4. Dashboard.tsx modifications
db_path = "src/components/Dashboard.tsx"

nav_old = """        {/* Global Nav Bar */}
        <nav className="navbar glass" style={{ background: 'var(--glass-bg)', padding: '0 1.5rem' }}>
           {/* 1. Workspace Name */}
           <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', minWidth: 0, flexShrink: 0 }}>
              {globalSettings?.logoUrlLight && (
                 <img src={theme === "light" ? globalSettings.logoUrlLight : (globalSettings.logoUrlDark || globalSettings.logoUrlLight)} alt="Logo" className="nav-logo" style={{ height: '40px', width: '40px', objectFit: 'contain', flexShrink: 0 }} />
              )}
              <h1 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 'bold', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {activeTab?.title ? `${activeTab.title} Dashboard` : (activeTheme.dashboardTitle || "Dashboard")}
              </h1>
           </div>

           {/* 2. Stretchable Search Bar */}
           <div style={{ flex: '1 1 0%', maxWidth: '1000px', margin: '0 1.5rem', position: 'relative', minWidth: '150px' }}>
              <div style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', opacity: 0.5 }}>
                 <Search size={18} />
              </div>
              <input 
                 type="text" 
                 placeholder="Search all apps & tools..." 
                 value={searchQuery}
                 onChange={e => setSearchQuery(e.target.value)}
                 style={{ 
                    width: '100%', padding: '0.7rem 1rem 0.7rem 2.8rem', 
                    background: 'rgba(255,255,255,0.06)', border: '1px solid var(--glass-border)', borderRadius: '999px',
                    color: 'var(--text)', outline: 'none', boxSizing: 'border-box',
                    transition: 'all 0.2s ease', backdropFilter: 'blur(10px)'
                 }} 
              />
           </div>

           {/* Right Group */}
           <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexShrink: 0 }}>"""

nav_new = """        {/* Global Nav Bar - Updated for Mobile / Multi-row */}
        <nav className="navbar glass" style={{ background: 'var(--glass-bg)', padding: '0.5rem 1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', height: 'auto', minHeight: 'var(--nav-height)' }}>
           {/* Top Row: Workspace + Mobile Menu/Right Buttons */}
           <div style={{ display: 'flex', width: '100%', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap' }}>
             {/* 1. Workspace Name */}
             <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', minWidth: 0, flexShrink: 0 }}>
                {globalSettings?.logoUrlLight && (
                   <img src={theme === "light" ? globalSettings.logoUrlLight : (globalSettings.logoUrlDark || globalSettings.logoUrlLight)} alt="Logo" className="nav-logo" style={{ height: '42px', width: 'auto', objectFit: 'contain', flexShrink: 0 }} />
                )}
                <h1 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 'bold', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {activeTab?.title ? `${activeTab.title} Dashboard` : (activeTheme.dashboardTitle || "Dashboard")}
                </h1>
             </div>

             {/* Right Group */}
             <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexShrink: 0, flexWrap: 'wrap' }}>"""

nav_end_old = """              <button title="Toggle Theme" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text)', padding: '0.5rem' }}>
                 {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
              </button>
           </div>
        </nav>"""

nav_end_new = """              <button title="Toggle Theme" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text)', padding: '0.5rem' }}>
                 {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
              </button>
             </div>
           </div>

           {/* 2. Search Bar Row (Moved Below Header) */}
           <div style={{ width: '100%', position: 'relative', marginTop: '0.25rem', marginBottom: '0.25rem' }}>
              <div style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', opacity: 0.5 }}>
                 <Search size={18} />
              </div>
              <input 
                 type="text" 
                 placeholder="Search all apps & tools..." 
                 value={searchQuery}
                 onChange={e => setSearchQuery(e.target.value)}
                 style={{ 
                    width: '100%', padding: '0.7rem 1rem 0.7rem 2.8rem', 
                    background: 'rgba(255,255,255,0.06)', border: '1px solid var(--glass-border)', borderRadius: '999px',
                    color: 'var(--text)', outline: 'none', boxSizing: 'border-box',
                    transition: 'all 0.2s ease', backdropFilter: 'blur(10px)'
                 }} 
              />
           </div>
        </nav>"""

add_bookmark_old = """                                      {showEditControls && (
                                         <div
                                            onClick={() => { setEditingBookmark({} as any); setTargetSectionIdForBookmark(section.id); setModalMode("add"); setIsBookmarkModalOpen(true); }}
                                            style={{ width: '100%', padding: '0.75rem', border: '1px dashed var(--glass-border)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', cursor: 'pointer', opacity: 0.5, transition: 'opacity 0.2s', marginTop: '0.25rem' }}
                                            onMouseEnter={e => e.currentTarget.style.opacity = '1'}
                                            onMouseLeave={e => e.currentTarget.style.opacity = '0.5'}
                                         >
                                            <Plus size={16} /> <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>Add Bookmark</span>
                                         </div>
                                      )}"""
add_bookmark_new = ""

patch_file(db_path, [
    (nav_old, nav_new),
    (nav_end_old, nav_end_new),
    (add_bookmark_old, add_bookmark_new)
])

print("UI Patch Complete.")
