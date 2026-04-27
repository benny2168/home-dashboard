import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

# 1. Update container padding
search_container = r'<div className="dashboard-container" style=\{\{ minHeight: \'100vh\', padding: \'1\.5rem 1\.25rem\', position: \'relative\', zIndex: 1 \}\}>'
replace_container = '<div className="dashboard-container" style={{ minHeight: \'100vh\', position: \'relative\', zIndex: 1 }}>'
content = re.sub(search_container, replace_container, content, count=1)

# 2. Build the new Header and Sticky Wrapper
search_header = r'<header className="dashboard-header" style=\{\{ maxWidth: `\$\{containerMaxWidth - 60\}px`, margin: \'0 auto 2rem auto\', display: \'flex\', alignItems: \'center\', justifyContent: \'space-between\', transition: \'all 0\.5s ease\' \}\}>'
replace_header = """<div className="sticky-control-bar" style={{
            position: 'sticky',
            top: 0,
            zIndex: 100,
            background: resolvedTheme === 'dark' ? 'rgba(15, 23, 42, 0.75)' : 'rgba(255, 255, 255, 0.85)',
            backdropFilter: 'blur(24px)',
            WebkitBackdropFilter: 'blur(24px)',
            borderBottom: '1px solid var(--glass-border)',
            paddingTop: '1.5rem',
            paddingLeft: '1.5rem',
            paddingRight: '1.5rem',
            boxShadow: '0 10px 40px rgba(0,0,0,0.05)'
         }}>
         <header className="dashboard-header" style={{ width: '100%', margin: '0 0 2rem 0', display: 'flex', alignItems: 'center', justifyContent: 'space-between', transition: 'all 0.5s ease' }}>"""
content = re.sub(search_header, replace_header, content, count=1)

# 3. Restructure `main`
search_main = r'</header>\s*<main style=\{\{ maxWidth: `\$\{containerMaxWidth - 60\}px`, margin: \'0 auto\', transition: \'all 0\.5s ease\' \}\}>\s*<div className="tabs-container" style=\{\{ marginBottom: \'2rem\' \}\}>'

replace_main = """</header>

         {/* Rest of the sticky bar (Search + Tabs) respects max width so it aligns with grid below */}
         <div style={{ maxWidth: `${containerMaxWidth - 60}px`, margin: '0 auto' }}>
            <div className="tabs-container">"""

content = re.sub(search_main, replace_main, content, count=1)

# 4. Close the sticky div AFTER the tabs
search_tabs_end = r'</button>\s*\)\}\s*</div>\s*\)\)}\s*\{showEditControls && \(\s*<button onClick=\{\(\) => \{ setEditingTabForModal\(null\); setLiveIconPreview\(null\); setIsTabModalOpen\(true\); \}\} className="btn" style=\{\{ padding: \'0\.5rem\', borderRadius: \'50%\', background: \'rgba\(255,255,255,0\.1\)\' \}\}>\s*<Plus size=\{18\} />\s*</button>\s*\)\}\s*</div>'

replace_tabs_end = """</button>
                  )}
</div>
              ))}
              {showEditControls && (
                <button onClick={() => { setEditingTabForModal(null); setLiveIconPreview(null); setIsTabModalOpen(true); }} className="btn" style={{ padding: '0.5rem', borderRadius: '50%', background: 'rgba(255,255,255,0.1)' }}>
                   <Plus size={18} />
                </button>
              )}
            </div>
         </div>
     </div>

     {/* Scrollable Content Container */}
     <main style={{ maxWidth: `${containerMaxWidth - 60}px`, margin: '2rem auto', transition: 'all 0.5s ease', padding: '0 1.25rem' }}>"""

content = re.sub(search_tabs_end, replace_tabs_end, content, count=1)


with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

