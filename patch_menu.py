#!/usr/bin/env python3

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

# 1. Add CSS definitions
old_css = """    :root, [data-theme='dark'], [data-theme='light'] {
      --primary: ${activeTheme.primaryColor};
      --primary-rgb: ${hexToRgb(activeTheme.primaryColor)};
      --primary-glow: rgba(${hexToRgb(activeTheme.primaryColor)}, 0.5);
      --glass-bg: ${glassBg};
      --glass-border: ${glassBorder};
    }"""

new_css = """    :root, [data-theme='dark'], [data-theme='light'] {
      --primary: ${activeTheme.primaryColor};
      --primary-rgb: ${hexToRgb(activeTheme.primaryColor)};
      --primary-glow: rgba(${hexToRgb(activeTheme.primaryColor)}, 0.5);
      --glass-bg: ${glassBg};
      --glass-border: ${glassBorder};
    }
    .desktop-nav-group { display: flex; }
    .mobile-menu-btn { display: none; }
    @media (max-width: 768px) {
      .desktop-nav-group { display: none !important; }
      .desktop-nav-group.open {
        display: flex !important;
        flex-direction: column;
        align-items: stretch !important;
        position: absolute;
        top: 4rem;
        right: 1.5rem;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        padding: 1rem;
        border-radius: 16px;
        z-index: 9999;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        backdrop-filter: blur(20px);
      }
      .mobile-menu-btn { display: flex !important; }
    }"""

# 2. Update Right Group wrapper
old_right_group = """             {/* Right Group */}
             <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexShrink: 0, flexWrap: 'wrap' }}>"""

new_right_group = """             {/* Mobile Menu Toggle */}
             <button className="mobile-menu-btn glass" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} style={{ padding: '0.5rem', borderRadius: '8px', border: '1px solid var(--glass-border)', background: 'transparent', color: 'var(--text)', cursor: 'pointer' }}>
                <LucideIcons.Menu size={20} />
             </button>

             {/* Right Group */}
             <div className={`desktop-nav-group ${isMobileMenuOpen ? 'open' : ''}`} style={{ alignItems: 'center', gap: '0.75rem', flexShrink: 0 }}>"""

content = content.replace(old_css, new_css)
content = content.replace(old_right_group, new_right_group)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

print("Menu patched!")
