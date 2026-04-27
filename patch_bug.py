#!/usr/bin/env python3

sm_path = "src/components/SectionModal.tsx"
with open(sm_path, "r") as f:
    content = f.read()

old_save = """      if (section) {
        await actions.updateSection(section.id, { title, icon, defaultCollapsed } as any);
      } else if (targetTabId) {
        const newSection = await actions.createSection({ title, icon, isGlobal: false, defaultCollapsed } as any);
        await actions.addSectionToTab(newSection.id, targetTabId);
      }"""

new_save = """      if (section) {
        await actions.updateSection(section.id, { title, icon } as any);
        if (targetTabId) await actions.updateTabSectionCollapsed(section.id, targetTabId, defaultCollapsed);
      } else if (targetTabId) {
        const newSection = await actions.createSection({ title, icon, isGlobal: false } as any);
        await actions.addSectionToTab(newSection.id, targetTabId);
        await actions.updateTabSectionCollapsed(newSection.id, targetTabId, defaultCollapsed);
      }"""

with open(sm_path, "w") as f:
    f.write(content.replace(old_save, new_save))

print("Section modal saving patched.")
