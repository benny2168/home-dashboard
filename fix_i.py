import sys
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

target = """Click "i" to open modal"""
replacement = """Click to view more info"""
content = content.replace(target, replacement)

with open(file_path, "w") as f: f.write(content)
print("replaced i text")
