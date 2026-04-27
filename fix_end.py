import sys, re
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

# We need to replace the closing `))` of dashboardColumns[colIdx].map((section) => { ...
# Let's find exactly lines ~1304
target = """                  </div>
                ))}
                {showEditControls && ("""

replacement = """                  </div>
                );
                })}
                {showEditControls && ("""

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, "w") as f: f.write(content)
    print("Fixed map closure")
else:
    print("Target not found.")

