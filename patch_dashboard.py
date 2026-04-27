#!/usr/bin/env python3
"""Replace the corrupted Main Content Area block in Dashboard.tsx with clean code."""

NEW_BLOCK = '''        {/* Main Content Area */}
        <div style={{ flex: 1, padding: '1.5rem', boxSizing: 'border-box', maxWidth: '1600px', margin: '0 auto', width: '100%', overflowX: 'hidden' }}>
           {displayedTabs.map(tab => (
              <div key={tab.id} style={{ marginBottom: '2rem' }}>
                 {searchQuery.trim() && <h2 style={{ marginBottom: '1rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem' }}>From {tab.title}</h2>}

                 {/* Multi-column layout: columns are side-by-side, sections stack vertically within each column */}
                 <div style={{
                    display: 'grid',
                    gridTemplateColumns: `repeat(${tab.columns || 3}, 1fr)`,
                    gap: '1rem', width: '100%', boxSizing: 'border-box', alignItems: 'start'
                 }}>
                    {Array.from({ length: tab.columns || 3 }, (_, colIdx) => (
                       <div key={colIdx} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', minWidth: 0 }}>
                          {tab.sections
                             .filter(s => (s.column ?? 0) === colIdx)
                             .sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
                             .map(section => (
                             <div
                                key={section.id}
                                draggable={showEditControls}
                                onDragStart={(e) => { if (showEditControls) { setDraggedSectionId(section.id); e.dataTransfer.effectAllowed = "move"; e.dataTransfer.setData("text/plain", section.id); e.stopPropagation(); } }}
                                onDragOver={(e) => { e.preventDefault(); e.dataTransfer.dropEffect = "move"; e.stopPropagation(); setDragOverSectionId(section.id); }}
                                onDragLeave={(e) => { if (!e.currentTarget.contains(e.relatedTarget as Node)) { setDragOverSectionId(null); } }}
                                onDragEnd={() => { setDraggedSectionId(null); setDragOverSectionId(null); }}
                                onDrop={(e) => { handleSectionDrop(e, section.id, tab.id); }}
                                style={{
                                   background: 'var(--glass-bg)', borderRadius: '16px',
                                   border: dragOverSectionId === section.id ? '2px dashed var(--primary)' : '1px solid var(--glass-border)',
                                   overflow: 'hidden', display: 'flex', flexDirection: 'column',
                                   height: 'fit-content', minWidth: 0, width: '100%', boxSizing: 'border-box',
                                   opacity: draggedSectionId === section.id ? 0.45 : 1,
                                   cursor: showEditControls ? 'grab' : 'default',
                                   transform: dragOverSectionId === section.id ? 'scale(1.02)' : 'none',
                                   transition: 'all 0.2s'
                                }}
                             >
                                {/* Section Header */}
                                <div style={{ padding: '0.75rem 1rem', background: 'rgba(0,0,0,0.1)', borderBottom: '1px solid var(--glass-border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                   <div onClick={() => toggleSection(tab.id, section.id, section.defaultCollapsed)} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', flex: 1, minWidth: 0 }}>
                                      <div style={{ flexShrink: 0, display: 'flex' }}>
                                         {(collapsedSections[`${tab.id}_${section.id}`] ?? section.defaultCollapsed) ? <ChevronRight size={16} /> : <ChevronDown size={16} />}
                                      </div>
                                      <div style={{ flexShrink: 0, display: 'flex' }}>
                                         <IconComponent name={section.icon || "LayoutGrid"} size={18} />
                                      </div>
                                      <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 600, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', flex: '1 1 auto', minWidth: 0 }}>{section.title}</h3>
                                   </div>
                                   {showEditControls && (
                                      <div style={{ display: 'flex', gap: '0.25rem' }}>
                                         <button onClick={() => { setEditingBookmark({} as any); setTargetSectionIdForBookmark(section.id); setModalMode("add"); setIsBookmarkModalOpen(true); }} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text)' }}><Plus size={16}/></button>
                                         <button onClick={() => { setEditingSection(section); setIsSectionModalOpen(true); }} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text)' }}><Settings size={16}/></button>
                                      </div>
                                   )}
                                </div>

                                {/* Bookmarks */}
                                {!(collapsedSections[`${tab.id}_${section.id}`] ?? section.defaultCollapsed) && (
                                   <div style={{ padding: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.25rem', overflowX: 'hidden', pointerEvents: draggedSectionId ? 'none' : 'auto' }}>
                                      {section.bookmarks.sort((a,b) => a.order - b.order).map(bookmark => (
                                         <div
                                            key={bookmark.id}
                                            draggable={showEditControls}
                                            onDragStart={(e) => { if (showEditControls) { setDraggedBookmarkId(bookmark.id); setDraggedBookmarkSectionId(section.id); e.dataTransfer.effectAllowed = "move"; e.dataTransfer.setData("text/plain", bookmark.id); e.stopPropagation(); } }}
                                            onDragOver={(e) => { e.preventDefault(); e.stopPropagation(); e.dataTransfer.dropEffect = "move"; setDragOverBookmarkId(bookmark.id); }}
                                            onDragLeave={(e) => { if (!e.currentTarget.contains(e.relatedTarget as Node)) setDragOverBookmarkId(null); }}
                                            onDragEnd={() => { setDraggedBookmarkId(null); setDraggedBookmarkSectionId(null); setDragOverBookmarkId(null); }}
                                            onDrop={(e) => handleBookmarkDrop(e, bookmark.id, section.id)}
                                            style={{ position: 'relative', width: '100%', boxSizing: 'border-box', minWidth: 0, opacity: draggedBookmarkId === bookmark.id ? 0.45 : 1, borderTop: dragOverBookmarkId === bookmark.id ? '2px solid var(--primary)' : '2px solid transparent' }}
                                         >
                                            <a href={showEditControls ? "#" : bookmark.url} target={showEditControls ? "_self" : (bookmark.openInNewTab !== false ? "_blank" : "_self")} style={{
                                               display: 'flex', alignItems: 'center', gap: '1rem', padding: '0.75rem', borderRadius: '12px', width: '100%', boxSizing: 'border-box', minWidth: 0,
                                               textDecoration: 'none', color: 'var(--text)', transition: 'background 0.2s', ...(!showEditControls ? { cursor: 'pointer' } : { cursor: 'grab' })
                                            }}
                                            onMouseEnter={e => e.currentTarget.style.background = 'rgba(150,150,150,0.1)'}
                                            onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                                            >
                                               <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '36px', height: '36px', borderRadius: '8px', background: 'rgba(var(--primary-rgb), 0.1)', color: 'var(--primary)', flexShrink: 0 }}>
                                                  <IconComponent name={bookmark.icon} size={20} />
                                               </div>
                                               <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden', flex: '1 1 auto', minWidth: 0 }}>
                                                  <span style={{ fontWeight: 600, fontSize: '0.95rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', display: 'block' }}>{bookmark.title}</span>
                                                  {bookmark.description ? <span style={{ fontSize: '0.8rem', opacity: 0.6, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', display: 'block' }}>{bookmark.description}</span> : null}
                                               </div>
                                            </a>
                                            {showEditControls && (
                                               <div style={{ position: 'absolute', right: '0.5rem', top: '50%', transform: 'translateY(-50%)', display: 'flex', gap: '0.25rem', background: 'var(--glass-bg)', padding: '0.25rem', borderRadius: '8px', border: '1px solid var(--glass-border)' }}>
                                                  <button onClick={(e) => { e.preventDefault(); setEditingBookmark(bookmark); setModalMode("edit"); setIsBookmarkModalOpen(true); }} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text)' }}><Edit2 size={14}/></button>
                                                  <button onClick={(e) => { e.preventDefault(); if(confirm('Delete app?')) actions.deleteBookmark(bookmark.id); }} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#ff4444' }}><Trash2 size={14}/></button>
                                               </div>
                                            )}
                                         </div>
                                      ))}
                                      {showEditControls && (
                                         <div
                                            onClick={() => { setEditingBookmark({} as any); setTargetSectionIdForBookmark(section.id); setModalMode("add"); setIsBookmarkModalOpen(true); }}
                                            style={{ width: '100%', padding: '0.75rem', border: '1px dashed var(--glass-border)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', cursor: 'pointer', opacity: 0.5, transition: 'opacity 0.2s', marginTop: '0.25rem' }}
                                            onMouseEnter={e => e.currentTarget.style.opacity = '1'}
                                            onMouseLeave={e => e.currentTarget.style.opacity = '0.5'}
                                         >
                                            <Plus size={16} /> <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>Add Bookmark</span>
                                         </div>
                                      )}
                                   </div>
                                )}
                             </div> /* end section card */
                          ))} {/* end sections.map */}
                       </div> {/* end column div */}
                    ))} {/* end Array.from columns */}

                    {showEditControls && (
                       <div
                          onClick={() => { setEditingSection(null); setIsSectionModalOpen(true); }}
                          style={{ background: 'transparent', borderRadius: '16px', border: '2px dashed var(--glass-border)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '150px', cursor: 'pointer', opacity: 0.5, transition: 'opacity 0.2s', color: 'var(--text)', gridColumn: '1 / -1' }}
                          onMouseEnter={e => e.currentTarget.style.opacity = '1'}
                          onMouseLeave={e => e.currentTarget.style.opacity = '0.5'}
                       >
                          <Plus size={24} style={{ marginBottom: '0.5rem' }} />
                          <span style={{ fontWeight: 600 }}>Add Section</span>
                       </div>
                    )}
                 </div> {/* end grid */}
              </div> {/* end tab block */}
           ))}
        </div> {/* end main content area */}

        {/* --- Modals --- */}
'''

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()
    lines = content.split('\n')

# Find boundaries
start_line = None
end_line = None
for i, line in enumerate(lines):
    if "{/* Main Content Area */}" in line:
        start_line = i
    if "{/* --- Modals --- */}" in line and start_line is not None:
        end_line = i
        break

if start_line is None or end_line is None:
    print(f"ERROR: Could not find markers. start={start_line}, end={end_line}")
    exit(1)

print(f"Replacing lines {start_line+1} to {end_line+1}")

new_lines = lines[:start_line] + [NEW_BLOCK] + lines[end_line+1:]
new_content = '\n'.join(new_lines)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(new_content)

print("Done!")
