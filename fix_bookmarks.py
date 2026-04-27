import sys, re
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

# 1. Replace showEditControls with isSectionEditable for bookmarks
# We'll isolate the chunk between `section.bookmarks.map((bookmark) => (` and `{showEditControls && !collapsedSections[section.id] && (`
start_marker = "{section.bookmarks.map((bookmark) => ("
end_marker = "{showEditControls && !collapsedSections[section.id] && ("

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    chunk = content[start_idx:end_idx]
    # In this chunk, replace all `showEditControls` with `isSectionEditable`
    chunk = chunk.replace("showEditControls", "isSectionEditable")
    content = content[:start_idx] + chunk + content[end_idx:]

# 2. Make lock icon clickable to open modal
target_lock = """<button disabled className="btn" style={{ padding: '6px', opacity: 0.5, cursor: 'not-allowed' }}><Lock size={14} /></button>"""
replacement_lock = """<button onClick={() => { setEditingSectionForModal(section); setLiveIconPreview(section.icon ?? null); setIsSectionModalOpen(true); }} className="btn" style={{ padding: '6px', opacity: 0.5, cursor: 'pointer' }}><Lock size={14} /></button>"""
content = content.replace(target_lock, replacement_lock)

# 3. Handle modal read-only fields and Remove button
target_modal_form = """          <div className="glass glass-card" style={{ width: '100%', maxWidth: '450px', padding: '2.5rem', border: '1px solid var(--glass-border)', boxShadow: '0 25px 50px rgba(0,0,0,0.25)' }}>
            <h2>{editingSectionForModal ? "Edit Section" : "Add Section"}</h2>
            <form action={async (formData) => {
              const title = formData.get("title") as string;"""

replacement_modal_form = """          <div className="glass glass-card" style={{ width: '100%', maxWidth: '450px', padding: '2.5rem', border: '1px solid var(--glass-border)', boxShadow: '0 25px 50px rgba(0,0,0,0.25)' }}>
            <h2>{editingSectionForModal ? (!canEditSection(editingSectionForModal) ? "Section Info (Read-Only)" : "Edit Section") : "Add Section"}</h2>
            <form action={async (formData) => {
              if (editingSectionForModal && !canEditSection(editingSectionForModal)) return; // Prevents dummy submits
              const title = formData.get("title") as string;"""
content = content.replace(target_modal_form, replacement_modal_form)

# Add readOnly properties to title
content = content.replace("""<input name="title" defaultValue={editingSectionForModal?.title} placeholder="Section Title" className="glass" style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem' }} required />""",
"""<input name="title" defaultValue={editingSectionForModal?.title} placeholder="Section Title" className="glass" style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', opacity: editingSectionForModal && !canEditSection(editingSectionForModal) ? 0.5 : 1 }} required readOnly={editingSectionForModal && !canEditSection(editingSectionForModal) ? true : false} />""")

target_modal_buttons = """                {editingSectionForModal && (
                  <button 
                    type="button" 
                    onClick={async () => { if(confirm('Delete section?')) { await actions.deleteSection(editingSectionForModal.id); window.location.reload(); } }}
                    className="btn glass" 
                    style={{ flex: 1, padding: '1rem', minWidth: '100px', background: 'rgba(239, 68, 68, 0.1)', color: '#ff4444', fontWeight: 600 }}
                  >
                    <Trash2 size={16} style={{ marginRight: '0.5rem' }} /> Delete
                  </button>
                )}
                <button type="submit" className="btn btn-primary" style={{ flex: 2, padding: '1rem', minWidth: '150px', fontWeight: 700 }}>Save Section</button>
"""

replacement_modal_buttons = """                {editingSectionForModal && (
                  <button 
                    type="button" 
                    onClick={async () => { if(confirm('Remove section from this workspace? (Does not delete it from database)')) { 
                       await actions.updateSectionLayout(editingSectionForModal.id, activeTabId, { remove: true } as any); 
                       window.location.reload(); 
                    } }}
                    className="btn glass" 
                    style={{ flex: 1, padding: '1rem', minWidth: '100px', background: 'rgba(239, 68, 68, 0.1)', color: '#ff4444', fontWeight: 600 }}
                  >
                    <Trash2 size={16} style={{ marginRight: '0.5rem' }} /> Remove
                  </button>
                )}
                {editingSectionForModal && (isAdmin || editingSectionForModal.owners?.some((o: any) => o.id === currentUserId) || canEditContent) && (
                  <button 
                    type="button" 
                    onClick={async () => { if(confirm('PERMANENTLY delete section from database? All bookmarks inside will be lost.')) { await actions.deleteSection(editingSectionForModal.id); window.location.reload(); } }}
                    className="btn glass" 
                    style={{ flex: 1, padding: '1rem', minWidth: '100px', background: 'rgba(239, 68, 68, 0.1)', color: '#ff4444', fontWeight: 600 }}
                  >
                    <Trash2 size={16} style={{ marginRight: '0.5rem' }} /> Delete
                  </button>
                )}
                {(!editingSectionForModal || canEditSection(editingSectionForModal)) && (
                   <button type="submit" className="btn btn-primary" style={{ flex: 2, padding: '1rem', minWidth: '150px', fontWeight: 700 }}>Save Section</button>
                )}
"""
content = content.replace(target_modal_buttons, replacement_modal_buttons)

with open(file_path, "w") as f: f.write(content)
print("Updated bookmarks logic and section modal.")
