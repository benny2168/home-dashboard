with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

import re

# 1. Revert the tab badge back to just Edit2 inside {showEditControls && activeTabId === tab.id && ( <button ... /> )}
badge_search_pattern = r"                  \{showEditControls && activeTabId === tab\.id && \(\s*<div style=\{\{\s*position: 'absolute',\s*top: '-8px',\s*right: '-6px',\s*display: 'flex',\s*gap: '4px',\s*zIndex: 10,\s*\}\}>\s*<button\s*onClick=\{\(\) => \{\s*setEditingTabForModal\(tab\);[\s\S]*?<Palette size=\{11\} />\s*</button>\s*</div>\s*\)\}"

badge_replacement = """                  {/* Edit tab overlay badge — only in edit mode */}
                  {showEditControls && activeTabId === tab.id && (
                    <button
                      onClick={() => {
                      setEditingTabForModal(tab);
                      setLiveIconPreview(tab.icon ?? null);
                      setTabModalTitle(tab.title);
                      setTabModalOrg(tab.organization || "");
                      setTabModalThemeId(tab.themeId || "");
                      setTabModalColumns(tab.columns || 3);
                      setTabModalIsLibrary(tab.isLibraryItem || false);
                      setTabModalDescription(tab.description || "");
                      setIsTabModalOpen(true);
                    }}
                      title="Edit this workspace"
                      style={{
                        position: 'absolute',
                        top: '-8px',
                        right: '-6px',
                        padding: '3px 5px',
                        borderRadius: '6px',
                        background: 'var(--primary)',
                        color: '#fff',
                        border: 'none',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        boxShadow: '0 2px 8px rgba(var(--primary-rgb), 0.4)',
                        zIndex: 10,
                        transition: 'transform 0.15s',
                      }}
                      onMouseEnter={(e) => (e.currentTarget.style.transform = 'scale(1.12)')}
                      onMouseLeave={(e) => (e.currentTarget.style.transform = 'scale(1)')}
                    >
                      <Edit2 size={11} />
                    </button>
                  )}"""

content = re.sub(badge_search_pattern, badge_replacement, content)


# 2. Add Palette button next to Browse Available Sections
search_bar_pattern = r"              \{showEditControls && \(\s*<button\s*onClick=\{\(\) => setIsLibraryOpen\(true\)\}\s*className=\"btn btn-primary\"\s*style=\{\{\s*padding: '0 1\.5rem', borderRadius: '16px', fontSize: '0\.9rem', fontWeight: 700,\s*display: 'flex', alignItems: 'center', gap: '0\.6rem',\s*whiteSpace: 'nowrap',\s*boxShadow: '0 8px 20px rgba\(var\(--primary-rgb\), 0\.3\)'\s*\}\}\s*>\s*<Library size=\{18\} />\s*Browse Available Sections\s*</button>\s*\)\}"

search_bar_replacement = """              {showEditControls && (
                 <div style={{ display: 'flex', gap: '0.75rem' }}>
                    <button 
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
                    </button>
                 </div>
              )}"""

content = re.sub(search_bar_pattern, search_bar_replacement, content)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)
