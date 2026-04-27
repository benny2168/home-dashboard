import sys
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

target = "editingSectionForModal && (isAdmin || editingSectionForModal.owners?.some((o: any) => o.id === currentUserId) || canEditContent) && ("
replacement = "editingSectionForModal && (isAdmin || editingSectionForModal.owners?.some((o: any) => o.id === currentUserId)) && ("
content = content.replace(target, replacement)

with open(file_path, "w") as f: f.write(content)
print("Removed canEditContent from Delete button")
