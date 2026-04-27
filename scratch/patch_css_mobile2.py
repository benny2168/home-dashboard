import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

# Bookmark Modal
content = content.replace(
    '''className="glass glass-card" style={{ width: '100%', maxWidth: '500px', padding: '2.5rem', maxHeight: '95vh', overflowY: 'auto', border: '1px solid var(--glass-border)', boxShadow: '0 25px 50px rgba(0,0,0,0.25)' }}''',
    '''className="glass glass-card modal-content" style={{ width: '100%', maxWidth: '500px', padding: '2.5rem', maxHeight: '95vh', overflowY: 'auto', border: '1px solid var(--glass-border)', boxShadow: '0 25px 50px rgba(0,0,0,0.25)' }}'''
)

# Workspace Modal
content = content.replace(
    '''className="glass glass-card" onClick={(e) => e.stopPropagation()} style={{ width: '100%', maxWidth: '520px', maxHeight: '90vh', overflowY: 'auto', border: '1px solid var(--glass-border)', boxShadow: '0 25px 50px rgba(0,0,0,0.25)', borderRadius: '20px', padding: 0 }}''',
    '''className="glass glass-card modal-content" onClick={(e) => e.stopPropagation()} style={{ width: '100%', maxWidth: '520px', maxHeight: '90vh', overflowY: 'auto', border: '1px solid var(--glass-border)', boxShadow: '0 25px 50px rgba(0,0,0,0.25)', borderRadius: '20px', padding: 0 }}'''
)

# Section Modal
content = content.replace(
    '''className="glass glass-card" style={{ width: '100%', maxWidth: '450px', padding: '2.5rem', border: '1px solid var(--glass-border)', boxShadow: '0 25px 50px rgba(0,0,0,0.25)' }}''',
    '''className="glass glass-card modal-content" style={{ width: '100%', maxWidth: '450px', padding: '2.5rem', border: '1px solid var(--glass-border)', boxShadow: '0 25px 50px rgba(0,0,0,0.25)' }}'''
)

# Catalog Modal
content = content.replace(
    '''className="glass" style={{ width: '100%', maxWidth: '1000px', maxHeight: '85vh', borderRadius: '32px', display: 'flex', flexDirection: 'column', overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.4)', border: '1px solid var(--glass-border)' }}''',
    '''className="glass modal-content" style={{ width: '100%', maxWidth: '1000px', maxHeight: '85vh', borderRadius: '32px', display: 'flex', flexDirection: 'column', overflow: 'hidden', boxShadow: '0 30px 60px rgba(0,0,0,0.4)', border: '1px solid var(--glass-border)' }}'''
)

# Bookmarks icon grid wrapper in Dashboard sections
# Needs to stop breaking horizontally inside sections.
# No wait! The bookmarks grid uses display: 'flex', flexWrap: 'wrap'. It shouldn't overflow... unless the `bookmark-wrapper` a tag has a minWidth... 
# "the sections and bookmarks are still a little wide on mobile, they extend beyond the screen."
# The only reason the section extends beyond the screen on mobile is the .dashboard-grid-wrapper!
# Let's ensure my previous patch hit it.

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

