import sys
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

target = "await actions.updateSectionLayout(editingSectionForModal.id, activeTabId, { remove: true } as any);"
replacement = "await actions.removeSectionFromTab(editingSectionForModal.id, activeTabId);"
content = content.replace(target, replacement)

with open(file_path, "w") as f: f.write(content)
print("Fixed remove button")
