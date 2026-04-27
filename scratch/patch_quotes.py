import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

content = content.replace("boxSizing: \"border-box\", width: \\'100%\\'", "boxSizing: 'border-box', width: '100%'")
content = content.replace("margin: \\'0 0 2rem 0\\'", "margin: '0 0 2rem 0'")
content = content.replace("flex: 1, position: \\'relative\\'", "flex: 1, position: 'relative'")
content = content.replace("padding: \\'1rem 1rem 1rem 3.5rem\\'", "padding: '1rem 1rem 1rem 3.5rem'")
content = content.replace("padding: \\'0.75rem 1rem\\'", "padding: '0.75rem 1rem'")
content = content.replace("overflowX: \\'hidden\\'", "overflowX: 'hidden'")
content = content.replace("position: \\'relative\\'", "position: 'relative'")
content = content.replace("paddingBottom: \\'2rem\\'", "paddingBottom: '2rem'")
content = content.replace("width: \\'100%\\'", "width: '100%'")

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

