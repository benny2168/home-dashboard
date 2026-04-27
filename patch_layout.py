#!/usr/bin/env python3
import os

# 1. Update globals.css to fix 100vw shifting bug and smaller tabs
css_path = "src/app/globals.css"
with open(css_path, "r") as f:
    css = f.read()

# Replace the 100vw width overrides that cause shifting to the right
css = css.replace("width: 100vw !important; max-width: 100vw !important;", "width: 100% !important; box-sizing: border-box !important;")

# Re-scale the tabs even smaller
css = css.replace(".workspace-tab-btn { padding: 0.4rem 0.75rem !important; font-size: 0.85rem !important; }", ".workspace-tab-btn { padding: 0.35rem 0.6rem !important; font-size: 0.75rem !important; }")

with open(css_path, "w") as f:
    f.write(css)

# 2. Fix AmbientBackground in Dashboard.tsx to be FIXED instead of ABSOLUTE so it doesn't get cut off when scrolling
dash_path = "src/components/Dashboard.tsx"
with open(dash_path, "r") as f:
    dash = f.read()

old_ambient = "      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', zIndex: 0, pointerEvents: 'none' }}>"
new_ambient = "      <div style={{ position: 'fixed', inset: 0, overflow: 'hidden', zIndex: 0, pointerEvents: 'none' }}>"
dash = dash.replace(old_ambient, new_ambient)

with open(dash_path, "w") as f:
    f.write(dash)

# 3. Add glow to LoginForm.tsx to incorporate themeColor
login_path = "src/app/login/LoginForm.tsx"
with open(login_path, "r") as f:
    login = f.read()

old_box_shadow = "boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.6)',"
new_box_shadow = "boxShadow: `0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 40px rgba(${themeRgb}, 0.2)`,"
login = login.replace(old_box_shadow, new_box_shadow)

with open(login_path, "w") as f:
    f.write(login)

print("Applied layout fixes: 100% width navbar, fixed ambient background, smaller tabs, login glow!")
