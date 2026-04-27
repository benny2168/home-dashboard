import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

old_snippet = "{isThemeModalOpen && <ThemeModal currentSettings={globalSettings} isOpen={isThemeModalOpen} onClose={() => setIsThemeModalOpen(false)} targetTabId={activeTab?.id} />}"
new_snippet = """{isThemeModalOpen && <ThemeModal 
            editingTheme={activeTheme} 
            isOpen={isThemeModalOpen} 
            onClose={() => setIsThemeModalOpen(false)} 
            onSave={async (data) => {
               if (activeTheme?.id) {
                  await actions.updateTheme(activeTheme.id, data);
               } else {
                  const newTheme = await actions.createTheme(data);
                  await actions.updateTab(activeTab.id, { themeId: newTheme.id });
               }
               setIsThemeModalOpen(false);
            }} 
         />}"""

content = content.replace(old_snippet, new_snippet)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

print("Patch Theme Model")
