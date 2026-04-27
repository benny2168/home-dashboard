with open('src/components/Dashboard.tsx', 'r') as f:
    text = f.read()

import re

# Remove any occurrences of:
#        <ThemeModal 
#            isOpen={isThemeModalOpen}
# ...
#            showCatalogToggle={true}
#        />
#

removal_pattern = r'       <ThemeModal[\s\S]*?showCatalogToggle=\{true\}\s*/>\s*'
cleaned = re.sub(removal_pattern, '', text)

# Now, add exactly one at the end of the return statement
final_insertion = """       <ThemeModal 
           isOpen={isThemeModalOpen}
           onClose={() => setIsThemeModalOpen(false)}
           editingTheme={activeTab?.theme || activeTheme}
           onSave={async (data) => {
               await actions.updateTabTheme(activeTabId, data);
               setIsThemeModalOpen(false);
               window.location.reload();
           }}
           showCatalogToggle={true}
       />
    </>
  );
}
"""

# Replace the end 
cleaned = re.sub(r'    </>\s*\);\s*}\s*$', final_insertion, cleaned)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(cleaned)
