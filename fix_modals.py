import sys
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

# Fix Modal Scrolling
target_modal = """<div className="modal-content glass" style={{ width: '100%', maxWidth: '500px', padding: '2rem', borderRadius: '16px', position: 'relative' }}"""
replacement_modal = """<div className="modal-content glass" style={{ width: '100%', maxWidth: '500px', padding: '1.5rem', borderRadius: '16px', position: 'relative', maxHeight: '85vh', overflowY: 'auto' }}"""
content = content.replace(target_modal, replacement_modal)

target_modal_600 = """<div className="modal-content glass" style={{ width: '100%', maxWidth: '600px', padding: '2rem', borderRadius: '16px', position: 'relative' }}"""
replacement_modal_600 = """<div className="modal-content glass" style={{ width: '100%', maxWidth: '600px', padding: '1.5rem', borderRadius: '16px', position: 'relative', maxHeight: '85vh', overflowY: 'auto' }}"""
content = content.replace(target_modal_600, replacement_modal_600)

target_modal_small = """<div className="modal-content glass" style={{ width: '100%', maxWidth: '400px', padding: '2rem', borderRadius: '16px', position: 'relative', textAlign: 'center' }}"""
replacement_modal_small = """<div className="modal-content glass" style={{ width: '100%', maxWidth: '400px', padding: '1.5rem', borderRadius: '16px', position: 'relative', textAlign: 'center', maxHeight: '85vh', overflowY: 'auto' }}"""
content = content.replace(target_modal_small, replacement_modal_small)

with open(file_path, "w") as f: f.write(content)
print("Fixed modal scrolling")
