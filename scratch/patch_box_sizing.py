import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

# 1. Header
search_header = r'<header className="dashboard-header" style=\{\{ width: \'100%\', margin: \'0 0 2rem 0\','
replace_header = r'<header className="dashboard-header" style={{ boxSizing: "border-box", width: \'100%\', margin: \'0 0 2rem 0\','
content = re.sub(search_header, replace_header, content)

# 2. Search Box Root
search_box = r'<div className="glass" style=\{\{ flex: 1, position: \'relative\', border:'
replace_box = r'<div className="glass" style={{ boxSizing: "border-box", flex: 1, position: \'relative\', border:'
content = re.sub(search_box, replace_box, content)

# 3. Search input
search_input = r'width: \'100%\', \n                    padding: \'1rem 1rem 1rem 3\.5rem\','
replace_input = r'boxSizing: "border-box", width: \'100%\', \n                    padding: \'1rem 1rem 1rem 3.5rem\','
content = re.sub(search_input, replace_input, content)

# 4. Mobile select
search_select = r'style=\{\{ width: \'100%\', padding: \'0\.75rem 1rem\','
replace_select = r'style={{ boxSizing: "border-box", width: \'100%\', padding: \'0.75rem 1rem\','
content = re.sub(search_select, replace_select, content)

# 5. Dashboard Grid Wrapper itself (just in case)
search_wrapper = r'className="dashboard-grid-wrapper" style=\{\{ overflowX: \'auto\', minWidth: 0, position: \'relative\', paddingBottom: \'2rem\' \}\}'
replace_wrapper = r'className="dashboard-grid-wrapper" style={{ boxSizing: "border-box", overflowX: \'hidden\', minWidth: 0, position: \'relative\', paddingBottom: \'2rem\', width: \'100%\' }}'
content = re.sub(search_wrapper, replace_wrapper, content)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

