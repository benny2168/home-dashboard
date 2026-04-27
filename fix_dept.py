import sys
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

target = """    // Dept level
    const deptRole = section.departmentAccess?.find((da: any) => da.department === userDepartment || da.department === "Entire Organization")?.role;
    if (deptRole === "owner" || deptRole === "editor") return true;"""

replacement = """    // Dept level
    const exactDeptMatch = section.departmentAccess?.find((da: any) => da.department === userDepartment);
    if (exactDeptMatch) {
        if (exactDeptMatch.role === "owner" || exactDeptMatch.role === "editor") return true;
        if (exactDeptMatch.role === "viewer") return false; // Explicit viewer restriction overrides global
    }
    const globalDeptMatch = section.departmentAccess?.find((da: any) => da.department === "Entire Organization");
    if (globalDeptMatch && (globalDeptMatch.role === "owner" || globalDeptMatch.role === "editor")) return true;"""

if target in content:
   content = content.replace(target, replacement)
   with open(file_path, "w") as f: f.write(content)
   print("Fixed dept role logic")
else:
   print("Target not found")
