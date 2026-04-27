import sys
file_path = "src/app/page.tsx"
with open(file_path, "r") as f: content = f.read()

target1 = """if (tab.departmentAccess?.some((da: any) => da.department === "Entire Organization" || da.department === userDepartment)) return true;"""
replacement1 = """if (tab.departmentAccess?.some((da: any) => da.department === "Entire Organization" || (da.department || "").toLowerCase().trim() === (userDepartment || "").toLowerCase().trim())) return true;"""

target2 = """if (section.departmentAccess?.some((da: any) => da.department === "Entire Organization" || da.department === userDepartment)) return true;"""
replacement2 = """if (section.departmentAccess?.some((da: any) => da.department === "Entire Organization" || (da.department || "").toLowerCase().trim() === (userDepartment || "").toLowerCase().trim())) return true;"""

content = content.replace(target1, replacement1)
content = content.replace(target2, replacement2)

with open(file_path, "w") as f: f.write(content)
