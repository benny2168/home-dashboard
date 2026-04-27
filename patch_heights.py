#!/usr/bin/env python3

import os

def patch_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: Could not find string in {filepath}")
    with open(filepath, 'w') as f:
        f.write(content)

# Fix IconPicker nested scroll heights
ip_path = "src/components/IconPicker.tsx"
patch_file(ip_path, [
    (
        "maxHeight: '180px', overflowY: 'auto'",
        "/* maxHeight removed to prevent nested scrollbars */"
    )
])

# Remove 300px limit from Modals
modals = ["BookmarkModal.tsx", "SectionModal.tsx", "TabModal.tsx"]
for modal in modals:
    p = f"src/components/{modal}"
    if os.path.exists(p):
        patch_file(p, [
            (
                "maxHeight: '300px', overflowY: 'auto'",
                "/* expanded dynamically */"
            )
        ])

print("Patched heights successfully!")
