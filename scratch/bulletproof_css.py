import re

with open("src/app/globals.css", "r") as f:
    css = f.read()

# We need to inject our block right before the closing bracket of @media (max-width: 768px)
# But there might be other media queries. We'll just search for a good place inside it.

injection = """
  /* BULLETPROOF MOBILE BOUNDS */
  body, html { overflow-x: hidden !important; width: 100% !important; max-width: 100% !important; margin: 0 !important; padding: 0 !important; }
  .dashboard-container { width: 100% !important; max-width: 100% !important; overflow-x: hidden !important; box-sizing: border-box !important; margin: 0 !important; padding: 0 !important; }
  .sticky-control-bar { padding-left: 1.25rem !important; padding-right: 1.25rem !important; width: 100% !important; max-width: 100% !important; box-sizing: border-box !important; margin: 0 !important; }
  .dashboard-header { width: 100% !important; max-width: 100% !important; box-sizing: border-box !important; margin-left: 0 !important; margin-right: 0 !important; }
  .tabs-container { width: 100% !important; max-width: 100% !important; padding: 0 !important; margin-left: 0 !important; margin-right: 0 !important; box-sizing: border-box !important; }
  .search-input, .mobile-tab-select select { max-width: 100% !important; box-sizing: border-box !important; }
  .dashboard-grid-wrapper { width: 100% !important; max-width: 100% !important; padding: 0 !important; margin: 0 !important; box-sizing: border-box !important; overflow: hidden !important; }
  main { width: 100% !important; max-width: 100% !important; padding: 0 1.25rem !important; box-sizing: border-box !important; margin-left: 0 !important; margin-right: 0 !important; }
  .dashboard-sections-grid { grid-template-columns: 1fr !important; width: 100% !important; min-width: 0 !important; max-width: 100% !important; box-sizing: border-box !important; padding: 0 !important; margin: 0 !important; }
  .glass-card { width: 100% !important; max-width: 100% !important; box-sizing: border-box !important; }
"""

# Find the end of the mobile media query
# Wait, let's just use regex to replace .dashboard-sections-grid inside the media query with our massive block.
search_pattern = r'\.dashboard-sections-grid \{\s*grid-template-columns: 1fr !important;\s*width: 100% !important;\s*min-width: 0 !important;\s*max-width: 100% !important;\s*\}'

if re.search(search_pattern, css):
    css = re.sub(search_pattern, injection, css)
else:
    print("Could not find pattern. Looking for alternative injection point.")
    # Alternate: find a place near .dashboard-grid-wrapper inside media query
    alt_search = r'\.dashboard-grid-wrapper \{\s*padding-bottom: 0\.5rem !important;\s*overflow-x: hidden !important; /\* No side scrolling on mobile \*/\s*\}'
    css = re.sub(alt_search, injection, css)

with open("src/app/globals.css", "w") as f:
    f.write(css)

