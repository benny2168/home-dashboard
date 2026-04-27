#!/usr/bin/env python3

with open('src/app/admin/AdminLayoutClient.tsx', 'r') as f:
    text = f.read()

# Fix the outer div and header
old_structure = """    <div className="fade-in admin-page" style={{ minHeight: '100vh', padding: '2rem' }}>
      <header className="admin-header glass" style={{ background: 'var(--glass-bg)', padding: 'calc(0.5rem + env(safe-area-inset-top)) 1.5rem 0.5rem 1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'sticky', top: 0, zIndex: 50, width: '100%', boxSizing: 'border-box', marginBottom: '2rem', backdropFilter: 'blur(20px)', borderBottom: '1px solid var(--glass-border)' }}>"""
new_structure = """    <div className="fade-in admin-page" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header className="admin-header glass" style={{ background: 'var(--glass-bg)', padding: 'calc(0.5rem + env(safe-area-inset-top)) 1.5rem 0.5rem 1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'sticky', top: 0, zIndex: 50, width: '100%', boxSizing: 'border-box', borderBottom: '1px solid var(--glass-border)', backdropFilter: 'blur(20px)' }}>"""
text = text.replace(old_structure, new_structure)

# Fix Logo sizes
old_logo_wide = """                  style={{ height: '28px', width: 'auto', objectFit: 'contain' }}"""
new_logo_wide = """                  style={{ height: '42px', width: 'auto', objectFit: 'contain' }}"""
text = text.replace(old_logo_wide, new_logo_wide)

# Fix title sizing to match Dashboard
old_title = """                <h1 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text)', margin: 0, lineHeight: 1 }}>
                    Admin Portal
                </h1>
                <span style={{ fontSize: '0.65rem', opacity: 0.4, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Settings
                </span>"""
new_title = """                <h1 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'var(--text)', margin: 0 }}>
                    Admin Portal
                </h1>"""
text = text.replace(old_title, new_title)

# Wrap inner admin grid with padding
old_grid = """      <div className="admin-grid" style={{ maxWidth: '1400px', margin: '0 auto', display: 'grid', gridTemplateColumns: '240px 1fr', gap: '2rem' }}>"""
new_grid = """      <div style={{ flex: 1, padding: '2rem', width: '100%', boxSizing: 'border-box' }}>
        <div className="admin-grid" style={{ maxWidth: '1400px', margin: '0 auto', display: 'grid', gridTemplateColumns: '240px 1fr', gap: '2rem' }}>"""
text = text.replace(old_grid, new_grid)

# Close the new padding div
old_footer = """      </div>

      <style jsx global>{`
        .fade-in { animation: fadeIn 0.4s ease-out; }"""
new_footer = """        </div>
      </div>

      <style jsx global>{`
        .fade-in { animation: fadeIn 0.4s ease-out; }"""
text = text.replace(old_footer, new_footer)

with open('src/app/admin/AdminLayoutClient.tsx', 'w') as f:
    f.write(text)

print("Admin structure patched successfully")
