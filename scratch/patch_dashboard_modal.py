import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

# 1. State setup
if 'const [catalogView,' not in content:
    content = content.replace(
        "const [isLibraryOpen, setIsLibraryOpen] = useState(false);",
        "const [isLibraryOpen, setIsLibraryOpen] = useState(false);\n  const [catalogView, setCatalogView] = useState<'sections'|'themes'>('sections');"
    )

# 2. Header replacement
header_search = r"\{\(globalSettings\.logoUrlLight \|\| globalSettings\.logoUrlDark\) && \([\s\S]*?\)\} \)}"

header_real_search = """            {(globalSettings.logoUrlLight || globalSettings.logoUrlDark) && (
              <>
                <img 
                  src={mounted && resolvedTheme === 'dark' 
                    ? (globalSettings.logoUrlDark || globalSettings.logoUrlLight || "")
                    : (globalSettings.logoUrlLight || globalSettings.logoUrlDark || "")
                  }
                  alt="System Logo"
                  className="logo-universal"
                  style={{ height: 'var(--logo-height, 50px)', width: 'auto', maxWidth: '200px', objectFit: 'contain', transition: 'all 0.4s ease' }}
                />
              </>
            )}"""

header_replace = """            {(() => {
               const customIcon = activeTab?.theme?.logoIcon || activeTheme?.logoIcon;
               if (customIcon) {
                   return (
                       <div className="logo-universal" style={{ height: 'var(--logo-height, 50px)', width: 'var(--logo-height, 50px)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                         <IconComponent name={customIcon} size={42} />
                       </div>
                   );
               }
               if (globalSettings.logoUrlLight || globalSettings.logoUrlDark) {
                   return (
                       <img 
                         src={mounted && resolvedTheme === 'dark' 
                           ? (globalSettings.logoUrlDark || globalSettings.logoUrlLight || "")
                           : (globalSettings.logoUrlLight || globalSettings.logoUrlDark || "")
                         }
                         alt="System Logo"
                         className="logo-universal"
                         style={{ height: 'var(--logo-height, 50px)', width: 'auto', maxWidth: '200px', objectFit: 'contain', transition: 'all 0.4s ease' }}
                       />
                   );
               }
               return null;
            })()}"""

content = content.replace(header_real_search, header_replace)

# 3. Button replacement
button_search = """                    <button 
                      onClick={() => setIsThemeModalOpen(true)}
                      className="btn"
                      style={{ 
                        padding: '0 1.25rem', borderRadius: '16px', fontSize: '0.9rem', fontWeight: 700, 
                        display: 'flex', alignItems: 'center', gap: '0.6rem',
                        background: 'rgba(var(--primary-rgb), 0.08)', color: 'var(--primary)',
                        border: '1px solid currentColor',
                        whiteSpace: 'nowrap',
                        transition: 'all 0.2s'
                      }}
                      title="Edit Workspace Theme"
                      onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(var(--primary-rgb), 0.15)')}
                      onMouseLeave={(e) => (e.currentTarget.style.background = 'rgba(var(--primary-rgb), 0.08)')}
                    >
                        <Palette size={18} />
                        Theme
                    </button>
                    <button 
                      onClick={() => setIsLibraryOpen(true)}
                      className="btn btn-primary"
                      style={{ 
                        padding: '0 1.5rem', borderRadius: '16px', fontSize: '0.9rem', fontWeight: 700, 
                        display: 'flex', alignItems: 'center', gap: '0.6rem',
                        whiteSpace: 'nowrap',
                        boxShadow: '0 8px 20px rgba(var(--primary-rgb), 0.3)'
                      }}
                    >
                        <Library size={18} />
                        Browse Available Sections
                    </button>"""

button_replace = """                    <button 
                      onClick={() => setIsThemeModalOpen(true)}
                      className="btn btn-primary"
                      style={{ 
                        padding: '0 1.25rem', borderRadius: '16px', fontSize: '0.9rem', fontWeight: 700, 
                        display: 'flex', alignItems: 'center', gap: '0.6rem',
                        whiteSpace: 'nowrap',
                        transition: 'all 0.2s',
                        background: 'linear-gradient(135deg, var(--primary), #8b5cf6)',
                        boxShadow: '0 8px 20px rgba(var(--primary-rgb), 0.4)',
                        border: 'none', color: '#fff'
                      }}
                      title="Edit Workspace Theme"
                    >
                        <Palette size={18} />
                        Theme
                    </button>
                    <button 
                      onClick={() => { setCatalogView('sections'); setIsLibraryOpen(true); }}
                      className="btn btn-primary"
                      style={{ 
                        padding: '0 1.5rem', borderRadius: '16px', fontSize: '0.9rem', fontWeight: 700, 
                        display: 'flex', alignItems: 'center', gap: '0.6rem',
                        whiteSpace: 'nowrap',
                        boxShadow: '0 8px 20px rgba(var(--primary-rgb), 0.3)'
                      }}
                    >
                        <Library size={18} />
                        Browse Catalog
                    </button>"""
content = content.replace(button_search, button_replace)

# 4. Catalog Replacement
catalog_search = r"\{\/\* --- SECTION CATALOG MODAL --- \*\/\}[\s\S]*?No shared toolsets are currently available in the catalog\.<\/p>\s*<\/div>\s*\)\}\s*<\/div>\s*<\/section>\s*<\/div>\s*<\/div>\s*<\/div>\s*\)\}"

catalog_replace = """{/* --- UNIFIED CATALOG MODAL --- */}
        {isLibraryOpen && (
           <div className="modal-overlay" style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(15px)', zIndex: 2000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
              <div className="glass" style={{ width: '100%', maxWidth: '1000px', maxHeight: '85vh', borderRadius: '32px', display: 'flex', flexDirection: 'column', overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.4)', border: '1px solid var(--glass-border)' }}>
                 <div style={{ padding: '2rem', borderBottom: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                       <div style={{ width: '48px', height: '48px', borderRadius: '16px', background: 'var(--primary)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 10px 20px rgba(var(--primary-rgb), 0.3)' }}>
                          <Library size={24} />
                       </div>
                       <div>
                          <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 800 }}>Catalog Library</h2>
                          <p style={{ margin: 0, opacity: 0.6, fontSize: '0.85rem' }}>Browse shared toolsets and workspace themes.</p>
                       </div>
                    </div>
                    <button onClick={() => setIsLibraryOpen(false)} className="btn" style={{ background: 'rgba(255,255,255,0.05)', color: 'var(--text)', border: '1px solid var(--glass-border)', borderRadius: '50%', width: '40px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                       <X size={18} />
                    </button>
                 </div>

                 {/* TOGGLE */}
                 <div style={{ padding: '1.5rem 2rem 0 2rem', display: 'flex', gap: '1rem', borderBottom: '1px solid var(--glass-border)' }}>
                    <button 
                       onClick={() => setCatalogView('sections')}
                       style={{ 
                          padding: '0.75rem 1.5rem', fontWeight: 700, fontSize: '0.9rem', background: 'transparent',
                          border: 'none', borderBottom: catalogView === 'sections' ? '3px solid var(--primary)' : '3px solid transparent',
                          color: catalogView === 'sections' ? 'var(--primary)' : 'var(--text)', opacity: catalogView === 'sections' ? 1 : 0.5,
                          cursor: 'pointer', transition: 'all 0.2s'
                        }}
                    >
                       Toolsets & Sections
                    </button>
                    <button 
                       onClick={() => setCatalogView('themes')}
                       style={{ 
                          padding: '0.75rem 1.5rem', fontWeight: 700, fontSize: '0.9rem', background: 'transparent',
                          border: 'none', borderBottom: catalogView === 'themes' ? '3px solid var(--primary)' : '3px solid transparent',
                          color: catalogView === 'themes' ? 'var(--primary)' : 'var(--text)', opacity: catalogView === 'themes' ? 1 : 0.5,
                          cursor: 'pointer', transition: 'all 0.2s'
                        }}
                    >
                       Workspace Themes
                    </button>
                 </div>

                 <div style={{ flex: 1, overflowY: 'auto', padding: '2rem' }}>
                    
                    {catalogView === 'sections' && (
                       <section>
                          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' }}>
                             {librarySections.map(ls => {
                                const isAlreadyInTab = activeTab?.sections.some(s => s.id === ls.id);
                                return (
                                   <div key={ls.id} className="glass" style={{ padding: '1.5rem', borderRadius: '20px', border: isAlreadyInTab ? '2px solid #4ade80' : '1px solid var(--glass-border)', display: 'flex', flexDirection: 'column', gap: '1rem', background: 'rgba(255,255,255,0.03)' }}>
                                      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                         <div style={{ width: '48px', height: '48px', borderRadius: '14px', background: 'rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
                                            <IconComponent name={ls.icon || "LayoutGrid"} size={24} />
                                         </div>
                                         <div>
                                            <h4 style={{ margin: 0, fontSize: '1.05rem', fontWeight: 700 }}>{ls.title}</h4>
                                            <span style={{ fontSize: '0.7rem', opacity: 0.5, fontWeight: 600 }}>{ls.organization || "Global"} Toolset</span>
                                         </div>
                                      </div>
                                      <p style={{ fontSize: '0.85rem', opacity: 0.6, margin: 0, minHeight: '3rem' }}>{ls.description || "A curated cluster of tools to boost your workflow."}</p>
                                      <button 
                                         disabled={isAlreadyInTab || importingSectionId === ls.id}
                                         onClick={async () => {
                                            if (!activeTabId) return;
                                            setImportingSectionId(ls.id);
                                            try {
                                               await actions.addSectionToTab(ls.id, activeTabId, 0);
                                               // Optimistic update
                                               const shapedSection = { ...ls, column: 0, height: null, tabId: activeTabId };
                                               setTabs(prev => prev.map(t => t.id === activeTabId ? { ...t, sections: [...t.sections, shapedSection] } : t));
                                               setJustImportedId(ls.id);
                                               setTimeout(() => setJustImportedId(null), 2000);
                                            } finally {
                                               setImportingSectionId(null);
                                            }
                                         }}
                                         className="btn btn-primary" 
                                         style={{ 
                                            marginTop: 'auto',
                                            padding: '0.75rem', borderRadius: '12px', fontWeight: 700, fontSize: '0.85rem',
                                            background: (isAlreadyInTab || justImportedId === ls.id) ? 'rgba(74, 222, 128, 0.1)' : 'var(--primary)',
                                            color: (isAlreadyInTab || justImportedId === ls.id) ? '#4ade80' : 'var(--nav-text)',
                                            border: (isAlreadyInTab || justImportedId === ls.id) ? '1px solid #4ade80' : 'none',
                                            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem'
                                         }}
                                      >
                                         {importingSectionId === ls.id ? "Adding..." : (isAlreadyInTab || justImportedId === ls.id) ? "Added!" : `Add to Workspace`}
                                      </button>
                                   </div>
                                );
                             })}
                             {librarySections.length === 0 && (
                                <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '3rem', opacity: 0.5 }}>
                                   <Library size={48} style={{ marginBottom: '1rem', opacity: 0.2 }} />
                                   <p>No shared toolsets are currently available in the catalog.</p>
                                </div>
                             )}
                          </div>
                       </section>
                    )}

                    {catalogView === 'themes' && (
                       <section>
                          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' }}>
                             {(allThemes || []).filter((t: any) => t.isLibraryItem).map((t: any) => {
                                const isActive = activeTab?.theme?.id === t.id && !activeTab?.theme?.owners?.some((o: any) => o.id === currentUserId);
                                return (
                                   <div key={t.id} className="glass" style={{ padding: '1.5rem', borderRadius: '20px', border: isActive ? `2px solid ${t.primaryColor}` : '1px solid var(--glass-border)', display: 'flex', flexDirection: 'column', gap: '1rem', background: 'rgba(255,255,255,0.03)' }}>
                                      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                         <div style={{ width: '48px', height: '48px', borderRadius: '14px', background: t.primaryColor, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', boxShadow: `0 4px 15px ${t.primaryColor}80` }}>
                                            <IconComponent name={t.logoIcon || "Palette"} size={24} />
                                         </div>
                                         <div>
                                            <h4 style={{ margin: 0, fontSize: '1.05rem', fontWeight: 700 }}>{t.name}</h4>
                                            <span style={{ fontSize: '0.7rem', opacity: 0.5, fontWeight: 600 }}>{t.dashboardTitle || "Workspace Theme"}</span>
                                         </div>
                                      </div>
                                      <p style={{ fontSize: '0.85rem', opacity: 0.6, margin: 0, minHeight: '3rem' }}>{t.description || "A beautiful curated theme shared with the organization."}</p>
                                      <button 
                                         disabled={isActive || importingSectionId === t.id}
                                         onClick={async () => {
                                            if (!activeTabId) return;
                                            setImportingSectionId(t.id);
                                            try {
                                               await actions.updateTabTheme(activeTabId, t);
                                               setIsLibraryOpen(false);
                                               window.location.reload();
                                            } finally {
                                               setImportingSectionId(null);
                                            }
                                         }}
                                         className="btn btn-primary" 
                                         style={{ 
                                            marginTop: 'auto',
                                            padding: '0.75rem', borderRadius: '12px', fontWeight: 700, fontSize: '0.85rem',
                                            background: isActive ? 'rgba(74, 222, 128, 0.1)' : t.primaryColor,
                                            color: isActive ? '#4ade80' : '#fff',
                                            border: isActive ? '1px solid #4ade80' : 'none',
                                            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem',
                                            textShadow: isActive ? 'none' : '0 1px 2px rgba(0,0,0,0.2)'
                                         }}
                                      >
                                         {importingSectionId === t.id ? "Applying..." : isActive ? "Active" : `Install Theme`}
                                      </button>
                                   </div>
                                );
                             })}
                             {!(allThemes || []).some((t: any) => t.isLibraryItem) && (
                                <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '3rem', opacity: 0.5 }}>
                                   <Palette size={48} style={{ marginBottom: '1rem', opacity: 0.2 }} />
                                   <p>No themes have been shared to the catalog yet.</p>
                                </div>
                             )}
                          </div>
                       </section>
                    )}
                 </div>
              </div>
           </div>
        )}"""
content = re.sub(catalog_search, catalog_replace, content)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

