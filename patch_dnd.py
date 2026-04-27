#!/usr/bin/env python3
"""Patch Dashboard.tsx to include optimistic dragndrop, inline add-section, and theme opacity"""

import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

# 1. Update handleSectionDrop
old_section_drop = """  const handleSectionDrop = async (e: React.DragEvent, targetId: string | undefined, currentTabId: string, colIdx: number) => {
     e.preventDefault();
     e.stopPropagation();
     const srcId = draggedSectionId;
     setDraggedSectionId(null);
     setDragOverSectionId(null);
     setDragOverColIdx(null);
     if (!srcId || srcId === targetId) return;
     await actions.moveSection(srcId, currentTabId, colIdx, targetId);
     router.refresh();
  };"""

new_section_drop = """  const handleSectionDrop = async (e: React.DragEvent, targetId: string | undefined, currentTabId: string, colIdx: number) => {
     e.preventDefault();
     e.stopPropagation();
     const srcId = draggedSectionId;
     setDraggedSectionId(null);
     setDragOverSectionId(null);
     setDragOverColIdx(null);
     if (!srcId || srcId === targetId) return;

     // Optimistic Local Update
     setTabs(currentTabs => {
        const newTabs = [...currentTabs];
        const tabIndex = newTabs.findIndex(t => t.id === currentTabId);
        if (tabIndex === -1) return currentTabs;
        const targetTab = { ...newTabs[tabIndex], sections: [...newTabs[tabIndex].sections] };
        
        const srcSectionIndex = targetTab.sections.findIndex(s => s.id === srcId);
        if (srcSectionIndex === -1) return currentTabs;
        
        const [movedSection] = targetTab.sections.splice(srcSectionIndex, 1);
        movedSection.column = colIdx;
        
        if (targetId) {
            const dstSectionIndex = targetTab.sections.findIndex(s => s.id === targetId);
            if (dstSectionIndex !== -1) {
                targetTab.sections.splice(dstSectionIndex, 0, movedSection);
            } else {
                targetTab.sections.push(movedSection);
            }
        } else {
            targetTab.sections.push(movedSection);
        }
        
        targetTab.sections.filter(s => s.column === colIdx).forEach((s, idx) => { s.order = idx; });
        newTabs[tabIndex] = targetTab;
        return newTabs;
     });

     await actions.moveSection(srcId, currentTabId, colIdx, targetId);
     // refresh in background without tearing UI
     router.refresh();
  };"""

content = content.replace(old_section_drop, new_section_drop)

# 2. Update handleBookmarkDrop
old_bookmark_drop = """  const handleBookmarkDrop = async (e: React.DragEvent, targetId: string, currentSectionId: string) => {
     e.preventDefault();
     e.stopPropagation();
     if (!draggedBookmarkId) return;
     if (draggedBookmarkId === targetId) { setDragOverBookmarkId(null); return; }
     
     // We do pessimistic updates for bookmarks right now 
     // unless we want to do a full deep clone of tabs which is verbose.
     await actions.moveBookmark(draggedBookmarkId, currentSectionId, targetId);
     setDraggedBookmarkId(null);
     setDraggedBookmarkSectionId(null);
     setDragOverBookmarkId(null);
     
     router.refresh();
  };"""

new_bookmark_drop = """  const handleBookmarkDrop = async (e: React.DragEvent, targetId: string, currentSectionId: string) => {
     e.preventDefault();
     e.stopPropagation();
     if (!draggedBookmarkId) return;
     if (draggedBookmarkId === targetId) { setDragOverBookmarkId(null); return; }
     
     const bId = draggedBookmarkId;
     setDraggedBookmarkId(null);
     setDraggedBookmarkSectionId(null);
     setDragOverBookmarkId(null);
     
     // Optimistic Local Update
     setTabs(currentTabs => {
         const newTabs = [...currentTabs];
         newTabs.forEach((tab, tIdx) => {
             const newSections = [...tab.sections];
             let changed = false;
             const srcSecIdx = newSections.findIndex(s => s.bookmarks.some(b => b.id === bId));
             const dstSecIdx = newSections.findIndex(s => s.id === currentSectionId);
             
             if (srcSecIdx !== -1 && dstSecIdx !== -1) {
                 changed = true;
                 const srcSec = { ...newSections[srcSecIdx], bookmarks: [...newSections[srcSecIdx].bookmarks] };
                 const dstSec = srcSecIdx === dstSecIdx ? srcSec : { ...newSections[dstSecIdx], bookmarks: [...newSections[dstSecIdx].bookmarks] };
                 
                 const bIdx = srcSec.bookmarks.findIndex(b => b.id === bId);
                 if (bIdx !== -1) {
                     const [moved] = srcSec.bookmarks.splice(bIdx, 1);
                     const targetBIdx = dstSec.bookmarks.findIndex(b => b.id === targetId);
                     if (targetBIdx !== -1) dstSec.bookmarks.splice(targetBIdx, 0, moved);
                     else dstSec.bookmarks.push(moved);
                     dstSec.bookmarks.forEach((b, i) => b.order = i);
                 }
                 newSections[srcSecIdx] = srcSec;
                 newSections[dstSecIdx] = dstSec;
             }
             if (changed) newTabs[tIdx] = { ...tab, sections: newSections };
         });
         return newTabs;
     });
     
     await actions.moveBookmark(bId, currentSectionId, targetId);
     router.refresh();
  };"""

content = content.replace(old_bookmark_drop, new_bookmark_drop)

# 3. Fix Theme Opacity
old_glass_bg = """  const isLight = theme === 'light';
  const glassBg = activeTheme.glassEffect === false ? 'var(--bg-color)' : 
      `linear-gradient(rgba(255, 255, 255, ${isLight ? 0.65 : 0.02}), rgba(255, 255, 255, ${isLight ? 0.65 : 0.02})), rgba(${hexToRgb(activeTheme.primaryColor)}, ${isLight ? 0.1 : 0.08})`;
  
  const glassBorder = activeTheme.glassEffect === false ? `rgba(${hexToRgb(activeTheme.primaryColor)}, 0.2)` : 
      `rgba(${hexToRgb(activeTheme.primaryColor)}, ${isLight ? 0.2 : 0.25})`;"""

new_glass_bg = """  const isLight = theme === 'light';
  const secOpac = activeTheme.sectionOpacity ?? 0.7;
  const glsOpac = activeTheme.glassOpacity ?? 0.12;

  // Use Theme sectionOpacity and glassOpacity logically synced to the slider range
  const glassOverlayAlpha = isLight ? (secOpac * 0.8) : (secOpac * 0.08); 
  const colorTintAlpha = isLight ? 0.1 : 0.08;

  const glassBg = activeTheme.glassEffect === false ? 'var(--bg-color)' : 
      `linear-gradient(rgba(255, 255, 255, ${glassOverlayAlpha}), rgba(255, 255, 255, ${glassOverlayAlpha})), rgba(${hexToRgb(activeTheme.primaryColor)}, ${colorTintAlpha})`;
  
  const glassBorder = activeTheme.glassEffect === false ? `rgba(${hexToRgb(activeTheme.primaryColor)}, 0.2)` : 
      `rgba(${hexToRgb(activeTheme.primaryColor)}, ${isLight ? 0.2 : 0.25})`;"""

content = content.replace(old_glass_bg, new_glass_bg)

# 4. Move Add Section box and Ghost area inside Col Mapping
# Let's cleanly replace the grid mapped area
old_cols_snippet = """                           ))}
                        </div>
                     ))}



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
                  </div>"""

new_cols_snippet = """                              {/* Drop placeholder (ghost area) inside column when dragging */}
                              {draggedSectionId && dragOverColIdx === colIdx && !dragOverSectionId && (
                                 <div style={{ width: '100%', height: '80px', borderRadius: '16px', border: '2px dashed var(--primary)', background: 'rgba(var(--primary-rgb), 0.1)' }} />
                              )}

                              {/* Add Section inside column */}
                              {showEditControls && (
                                 <div
                                    onClick={() => { setEditingSection(null); setIsSectionModalOpen(true); }}
                                    style={{ background: 'transparent', borderRadius: '16px', border: '1px dashed var(--glass-border)', display: 'flex', flexDirection: 'column', gap: '0.25rem', alignItems: 'center', justifyContent: 'center', padding: '1rem', cursor: 'pointer', opacity: 0.5, transition: 'opacity 0.2s', color: 'var(--text)', marginTop: '0.5rem' }}
                                    onMouseEnter={e => e.currentTarget.style.opacity = '1'}
                                    onMouseLeave={e => e.currentTarget.style.opacity = '0.5'}
                                 >
                                    <Plus size={16} />
                                    <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>Add Section</span>
                                 </div>
                              )}
                           </div>
                        ))}
                  </div>"""

if old_cols_snippet not in content:
    old_cols_snippet = old_cols_snippet.replace('   ', '  ')
    old_cols_snippet = old_cols_snippet.replace('\n\n\n\n', '\n\n')

content = content.replace(old_cols_snippet, new_cols_snippet)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

print("Patch complete.")
