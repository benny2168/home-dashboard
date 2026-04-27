#!/usr/bin/env python3
import os

# 1. Update globals.css with strict mobile resets
css_path = "src/app/globals.css"
with open(css_path, "r") as f:
    css = f.read()

mobile_fixes = """
/* ---- MOBILE FIXES ---- */
@media (max-width: 768px) {
  /* Edge to edge header */
  .navbar { padding-left: 0.5rem !important; padding-right: 0.5rem !important; border-left: none !important; border-right: none !important; border-radius: 0 !important; width: 100vw !important; max-width: 100vw !important; }
  .admin-header { padding-left: 0.5rem !important; padding-right: 0.5rem !important; border-left: none !important; border-right: none !important; border-radius: 0 !important; width: 100vw !important; max-width: 100vw !important; }
  
  /* Reduced gap and padding for sections */
  .dashboard-main-content { padding: 0.25rem !important; }
  .dashboard-grid { gap: 0.5rem !important; }
  
  /* Tabs scaling */
  .workspace-tab-btn { padding: 0.4rem 0.75rem !important; font-size: 0.85rem !important; }
  .workspace-tab-container { padding: 0.5rem 0 0 0 !important; }
}

/* Fix weird vertical scrollbar caused by bottom margin pushing into overflow container */
.tab-scroll-container {
  overflow-y: hidden !important;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.tab-scroll-container::-webkit-scrollbar { display: none; }
"""

if "/* ---- MOBILE FIXES ---- */" not in css:
    css += mobile_fixes

with open(css_path, "w") as f:
    f.write(css)


# 2. Update Dashboard.tsx tabs & padding
dash_path = "src/components/Dashboard.tsx"
with open(dash_path, "r") as f:
    dash = f.read()

# Tab container replacement
old_tab_wrapper = """         {(tabs.length > 1 || showEditControls) && !searchQuery.trim() && (
            <div style={{ width: '100%', boxSizing: 'border-box', overflowX: 'auto', borderBottom: '1px solid var(--glass-border)', background: 'transparent' }}>
               <div style={{ display: 'flex', padding: '1.2rem 1.5rem 0 1.5rem', gap: '0.2rem', maxWidth: '1600px', margin: '0 auto', alignItems: 'flex-end', justifyContent: 'flex-start' }}>"""
new_tab_wrapper = """         {(tabs.length > 1 || showEditControls) && !searchQuery.trim() && (
            <div className="tab-scroll-container" style={{ width: '100%', boxSizing: 'border-box', overflowX: 'auto', borderBottom: '1px solid var(--glass-border)', background: 'transparent' }}>
               <div className="workspace-tab-container" style={{ display: 'flex', padding: '1.2rem 1.5rem 0 1.5rem', gap: '0.2rem', maxWidth: '1600px', margin: '0 auto', alignItems: 'flex-end', justifyContent: 'flex-start' }}>"""
dash = dash.replace(old_tab_wrapper, new_tab_wrapper)

# Tab button replacement
old_tab_btn = """                        style={{ 
                           padding: '0.75rem 1.25rem',
                           background: dragOverTabId === tab.id ? 'rgba(var(--primary-rgb), 0.2)' : activeTabId === tab.id ? 'var(--primary)' : 'var(--glass-bg)',"""
new_tab_btn = """                        className="workspace-tab-btn"
                        style={{ 
                           padding: '0.75rem 1.25rem',
                           background: dragOverTabId === tab.id ? 'rgba(var(--primary-rgb), 0.2)' : activeTabId === tab.id ? 'var(--primary)' : 'var(--glass-bg)',"""
dash = dash.replace(old_tab_btn, new_tab_btn)

# Also fix the Add Workspace button tab
old_add_tab = """                     <button 
                        onClick={() => { setTargetTabToEdit(null); setIsTabModalOpen(true); }}
                        style={{ 
                           padding: '0.75rem 1.25rem', background: 'transparent', border: '1px dashed var(--glass-border)', borderBottom: 'none',"""
new_add_tab = """                     <button 
                        className="workspace-tab-btn"
                        onClick={() => { setTargetTabToEdit(null); setIsTabModalOpen(true); }}
                        style={{ 
                           padding: '0.75rem 1.25rem', background: 'transparent', border: '1px dashed var(--glass-border)', borderBottom: 'none',"""
dash = dash.replace(old_add_tab, new_add_tab)

with open(dash_path, "w") as f:
    f.write(dash)

print("CSS and Dashboard specific mobile sizing fixes applied!")
