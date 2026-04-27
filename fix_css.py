import sys
file_path = "src/app/globals.css"
with open(file_path, "r") as f: content = f.read()

target1 = """  .dashboard-container { 
    padding: 1.25rem 0.75rem !important; 
    max-width: calc(100% - 24px) !important;
    margin: 0 auto !important;
  }"""

replacement1 = """  .dashboard-container { 
    padding: 1rem 0 !important; 
    width: 100% !important;
    max-width: 100vw !important;
    margin: 0 !important;
    overflow-x: hidden !important;
  }
  
  .dashboard-header {
     padding: 0 1rem !important;
     width: 100% !important;
     box-sizing: border-box !important;
  }
  
  .dashboard-grid-wrapper {
     padding: 0 0.5rem !important;
     width: 100vw !important;
     box-sizing: border-box !important;
  }
  
  .glass-card {
     width: 100% !important;
     box-sizing: border-box !important;
  }"""

content = content.replace(target1, replacement1)

target2 = """  .logo-wide { display: none !important; }
  .logo-square { display: block !important; }"""

replacement2 = """  .logo-universal { --logo-height: 38px; }"""

content = content.replace(target2, replacement2).replace(target2, replacement2) # In case it's there twice

with open(file_path, "w") as f: f.write(content)
print("Fixed globals.css")
