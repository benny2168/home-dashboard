#!/usr/bin/env python3

import os

# 1. Update Dashboard.tsx
dash_path = "src/components/Dashboard.tsx"
with open(dash_path, "r") as f:
    dash = f.read()

old_dash_nav = """         <nav className="navbar glass" style={{ background: 'var(--glass-bg)', padding: '0.5rem 1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', height: 'auto', minHeight: 'var(--nav-height)' }}>"""
new_dash_nav = """         <nav className="navbar glass" style={{ background: 'var(--glass-bg)', padding: 'calc(0.5rem + env(safe-area-inset-top)) 1.5rem 0.5rem 1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', height: 'auto', minHeight: 'var(--nav-height)', position: 'sticky', top: 0, zIndex: 50, width: '100%', boxSizing: 'border-box', backdropFilter: 'blur(20px)' }}>"""
dash = dash.replace(old_dash_nav, new_dash_nav)

old_dash_main = """         <div style={{ flex: 1, padding: '1.5rem', boxSizing: 'border-box', maxWidth: '1600px', margin: '0 auto', width: '100%', overflowX: 'hidden' }}>"""
new_dash_main = """         <div className="dashboard-main-content" style={{ flex: 1, padding: '1.5rem', boxSizing: 'border-box', maxWidth: '1600px', margin: '0 auto', width: '100%', overflowX: 'hidden' }}>"""
dash = dash.replace(old_dash_main, new_dash_main)

with open(dash_path, "w") as f:
    f.write(dash)

# 2. Update globals.css with dashboard-main-content mobile padding
css_path = "src/app/globals.css"
with open(css_path, "r") as f:
    css = f.read()
if "dashboard-main-content" not in css:
    css_injection = """
@media (max-width: 768px) {
  .dashboard-main-content { padding: 0.5rem !important; }
}
"""
    css += css_injection
with open(css_path, "w") as f:
    f.write(css)

# 3. Update AdminLayoutClient.tsx
admin_path = "src/app/admin/AdminLayoutClient.tsx"
with open(admin_path, "r") as f:
    admin = f.read()

old_admin_header = """      <header className="admin-header" style={{ maxWidth: '1400px', margin: '0 auto 2rem auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>"""
new_admin_header = """      <header className="admin-header glass" style={{ background: 'var(--glass-bg)', padding: 'calc(0.5rem + env(safe-area-inset-top)) 1.5rem 0.5rem 1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'sticky', top: 0, zIndex: 50, width: '100%', boxSizing: 'border-box', marginBottom: '2rem', backdropFilter: 'blur(20px)', borderBottom: '1px solid var(--glass-border)' }}>"""
admin = admin.replace(old_admin_header, new_admin_header)

with open(admin_path, "w") as f:
    f.write(admin)

print("Headers and grid updated successfully!")
