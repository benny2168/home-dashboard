import sys, re
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

# 1. Update the tooltip CSS so the hover tooltip works for the Lock icon
if ".tooltip-container:hover .tooltip-bubble" not in content:
    css_target = "          box-shadow: none;"
    css_insert = """          box-shadow: none;
        }
        .tooltip-container:hover .tooltip-bubble {
            visibility: visible !important;
            opacity: 1 !important;
        }"""
    content = content.replace(css_target, css_insert)

# 2. Add isSectionEditable inside the section map loops
# We need to replace instances of showEditControls with isSectionEditable inside the section iteration
section_map_target = "                {dashboardColumns[colIdx].map((section) => ("
section_map_replacement = """                {dashboardColumns[colIdx].map((section) => {
                  const isSectionEditable = showEditControls && canEditSection(section);
                  return ("""

if section_map_replacement not in content:
    content = content.replace(section_map_target, section_map_replacement)

# Update the end of the section map
section_map_end_target = """                      </>
                    )}
                  </div>
                ))}
              </div>"""
section_map_end_replacement = """                      </>
                    )}
                  </div>
                );
                })}
              </div>"""
content = content.replace(section_map_end_target, section_map_end_replacement)

# Replace 'showEditControls' with 'isSectionEditable' for all bookmark/section internal logic 
# We'll use regex to only do it inside the section loop. 
# But wait, it's safer to just replace it manually in python by chunk replacing.
# Actually, the user can just use sed/regex.
# A simpler way: we'll replace all showEditControls in the block between `<div key={section.id}` and `</>` with isSectionEditable.
# Wait, I don't want to mess up. I'll just write the exact replacements.

with open(file_path, "w") as f: f.write(content)
