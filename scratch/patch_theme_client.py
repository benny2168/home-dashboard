import re

with open('src/app/admin/theme/ThemeClient.tsx', 'r') as f:
    content = f.read()

# Add import
if 'import ThemeModal' not in content:
    content = content.replace('import * as actions from "@/app/admin/actions";', 'import * as actions from "@/app/admin/actions";\nimport ThemeModal from "@/components/ThemeModal";')

# We need to wipe lines 43 to right before handleGlobalUpdate (around line 422)
# BUT we need to keep state variables that are used in the parent:
# themes, globalBrand, isModalOpen, isDeleteModalOpen, editingTheme, searchQuery, viewMode, collapsedDepts, modifiedDepts

state_repl = """  const [themes, setThemes] = useState(initialThemes);
  const [globalBrand, setGlobalBrand] = useState(globalSettings);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTheme, setEditingTheme] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState<"grid" | "matrix">("grid");
  const [collapsedDepts, setCollapsedDepts] = useState<string[]>([]);
  const [modifiedDepts, setModifiedDepts] = useState<Record<string, string>>({}); // key: dept_themeId

  const [stagedSystemColor, setStagedSystemColor] = useState(globalSettings.systemThemeColor);
  const [isApplyingColor, setIsApplyingColor] = useState(false);

  // Helper for high-contrast text over theme colors
  function getContrastText(hexcolor: string) {
    if (!hexcolor || hexcolor.length < 7) return '#fff';
    const r = parseInt(hexcolor.substring(1, 3), 16);
    const g = parseInt(hexcolor.substring(3, 5), 16);
    const b = parseInt(hexcolor.substring(5, 7), 16);
    const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
    if (yiq >= 128) return 'var(--text)';
    return '#fff';
  }

  const openAdd = () => {
    setEditingTheme(null);
    setIsModalOpen(true);
  };

  const openEdit = (theme: any) => {
    setEditingTheme(theme);
    setIsModalOpen(true);
  };

  const saveTheme = async (data: any) => {
    if (editingTheme) {
      await actions.updateTheme(editingTheme.id, data);
    } else {
      await actions.createTheme(data);
    }
    window.location.reload();
  };

  const deleteSelectedTheme = async () => {
      if (editingTheme) {
          await actions.deleteTheme(editingTheme.id);
          window.location.reload();
      }
  };
"""

content = re.sub(r'// --- Random Theme Name Generator ---.*?const handleGlobalUpdate = async ', state_repl + '\n  const handleGlobalUpdate = async ', content, flags=re.DOTALL)

# Replace the modal HTML at the end, starting from {isModalOpen && (
modal_repl = """       <ThemeModal 
           isOpen={isModalOpen}
           onClose={() => setIsModalOpen(false)}
           editingTheme={editingTheme}
           onSave={saveTheme}
           onDelete={deleteSelectedTheme}
           showCatalogToggle={true}
       />
"""

content = re.sub(r'\{isModalOpen && \(\n.*?<div className="modal-overlay".*?\{/\* DELETE CONFIRMATION MODAL \*/\}[\s\S]*?\{isDeleteModalOpen && \([\s\S]*?\)\}', modal_repl, content, flags=re.DOTALL)

with open('src/app/admin/theme/ThemeClient.tsx', 'w') as f:
    f.write(content)
