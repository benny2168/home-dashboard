import sqlite3, json
conn = sqlite3.connect('prisma/dev.db')
c = conn.cursor()
c.execute("SELECT id FROM Section WHERE title LIKE '%helpful hints%' LIMIT 1")
row = c.fetchone()
if not row:
    print("Section not found")
else:
    sec_id = row[0]
    print(f"Section ID: {sec_id}")
    c.execute("SELECT department, role FROM DepartmentAccess WHERE sectionId = ?", (sec_id,))
    print("Dept Access:", c.fetchall())
    c.execute("SELECT B FROM _SectionOwners WHERE A = ?", (sec_id,))
    print("Owners:", c.fetchall())
    c.execute("SELECT B FROM _SectionEditors WHERE A = ?", (sec_id,))
    print("Editors:", c.fetchall())
