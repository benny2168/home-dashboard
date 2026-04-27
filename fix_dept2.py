import sys
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

target = """    // Dept level
    const exactDeptMatch = section.departmentAccess?.find((da: any) => da.department === userDepartment);"""

replacement = """    // Dept level
    const normUserDept = (userDepartment || "").toLowerCase().trim();
    const exactDeptMatch = section.departmentAccess?.find((da: any) => (da.department || "").toLowerCase().trim() === normUserDept);"""
    
content = content.replace(target, replacement)

with open(file_path, "w") as f: f.write(content)
