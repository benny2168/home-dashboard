import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

# 1. Fix grid padding on mobile by stripping destructive inline margins
search_wrapper = r'className="dashboard-grid-wrapper" style=\{\{ overflowX: \'auto\', minWidth: 0, position: \'relative\', paddingBottom: \'2rem\', paddingRight: \'1rem\', marginLeft: \'-1rem\', paddingLeft: \'1rem\' \}\}'
replace_wrapper = 'className="dashboard-grid-wrapper" style={{ overflowX: \'auto\', minWidth: 0, position: \'relative\', paddingBottom: \'2rem\' }}'
content = re.sub(search_wrapper, replace_wrapper, content)

# 2. Add 'modal-content' to Edit Modals to respect CSS max widths on mobile
search_modals = r'className="glass" style=\{\{ padding: \'2rem\', borderRadius: \'24px\', width: \'100%\', maxWidth: \'600px\''
replace_modals = 'className="glass modal-content" style={{ padding: \'2rem\', borderRadius: \'24px\', width: \'100%\', maxWidth: \'600px\''
content = re.sub(search_modals, replace_modals, content)

search_tab_modals = r'className="glass code-card" style=\{\{ width: \'100%\', maxWidth: \'1000px\','
replace_tab_modals = 'className="glass code-card modal-content" style={{ width: \'100%\', maxWidth: \'1000px\','
content = re.sub(search_tab_modals, replace_tab_modals, content)

search_section_modals = r'className="glass" style=\{\{ width: \'100%\', maxWidth: \'600px\', maxHeight: \'85vh\','
replace_section_modals = 'className="glass modal-content" style={{ width: \'100%\', maxWidth: \'600px\', maxHeight: \'85vh\','
content = re.sub(search_section_modals, replace_section_modals, content)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

with open("src/components/ThemeModal.tsx", "r") as f:
    theme_content = f.read()

# Also fix Theme Modal
theme_search = r'className="glass fade-in" style=\{\{ width: \'100%\', maxWidth: \'800px\', padding: \'2\.5rem\','
theme_replace = 'className="glass fade-in modal-content" style={{ width: \'100%\', maxWidth: \'800px\', padding: \'2.5rem\','
theme_content = re.sub(theme_search, theme_replace, theme_content)

with open("src/components/ThemeModal.tsx", "w") as f:
    f.write(theme_content)

