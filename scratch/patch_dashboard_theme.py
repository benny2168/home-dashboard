import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Add imports
if 'import ThemeModal' not in content:
    content = content.replace('import { IconComponent } from "./IconPicker";', 'import { IconComponent } from "./IconPicker";\nimport ThemeModal from "@/components/ThemeModal";')

if 'Palette' not in content:
    content = content.replace('X,\n  Upload,', 'X,\n  Upload,\n  Palette,')

# Add state isThemeModalOpen 
if 'const [isThemeModalOpen, setIsThemeModalOpen]' not in content:
    content = content.replace('const [isTabModalOpen, setIsTabModalOpen] = useState(false);', 'const [isTabModalOpen, setIsTabModalOpen] = useState(false);\n  const [isThemeModalOpen, setIsThemeModalOpen] = useState(false);')

# Replace the edit tab badge to include palette 
badge_search = """                  {showEditControls && activeTabId === tab.id && (
                    <button
                      onClick={() => {"""

badge_repl = """                  {showEditControls && activeTabId === tab.id && (
                    <div style={{
                        position: 'absolute',
                        top: '-8px',
                        right: '-6px',
                        display: 'flex',
                        gap: '4px',
                        zIndex: 10,
                    }}>
                    <button
                      onClick={() => {"""

if 'Palette size={11} ' not in content:
    content = content.replace(badge_search, badge_repl)
    
    btn_end_search = """                      <Edit2 size={11} />
                    </button>
                  )}"""
    btn_end_repl = """                      <Edit2 size={11} />
                    </button>
                    <button
                        onClick={() => setIsThemeModalOpen(true)}
                        title="Edit Workspace Theme"
                        style={{
                          padding: '3px 5px',
                          borderRadius: '6px',
                          background: 'var(--primary)',
                          color: '#fff',
                          border: 'none',
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          boxShadow: '0 2px 8px rgba(var(--primary-rgb), 0.4)',
                          transition: 'transform 0.15s',
                        }}
                        onMouseEnter={(e) => (e.currentTarget.style.transform = 'scale(1.12)')}
                        onMouseLeave={(e) => (e.currentTarget.style.transform = 'scale(1)')}
                      >
                        <Palette size={11} />
                      </button>
                    </div>
                  )}"""
    content = content.replace(btn_end_search, btn_end_repl)

# Add ThemeModal component at the end
modal_addition = """       <ThemeModal 
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
"""

if '<ThemeModal' not in content:
    content = content.replace('        )}', '        )}\n' + modal_addition)


with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)

