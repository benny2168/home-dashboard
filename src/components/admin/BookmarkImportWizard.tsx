"use client";

import { useState, useRef } from "react";
import { Upload, ArrowRight, Check, X, Loader2, FolderOpen, Bookmark as BookmarkIcon } from "lucide-react";
import * as actions from "@/app/admin/actions";

interface Props {
  tabs: any[];
}

export function BookmarkImportWizard({ tabs }: Props) {
  const [step, setStep] = useState(1); // 1: Upload, 2: Mapping, 3: Success
  const [isScanning, setIsScanning] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [folders, setFolders] = useState<any[]>([]);
  const [mappings, setMappings] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsScanning(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const discoveredFolders = await actions.scanBookmarksFile(formData);
      
      setFolders(discoveredFolders as any[]);
      // Initialize mappings: default to 'skip'
      setMappings((discoveredFolders as any[]).map((f: any) => ({
        folderName: f.name,
        targetType: 'skip',
        targetSectionId: '',
        newSectionTitle: f.name,
        newTabId: tabs[0]?.id || '',
        bookmarks: f.bookmarks
      })));
      setStep(2);
    } catch (err: any) {
      setError(err.message || "Failed to scan file");
    } finally {
      setIsScanning(false);
    }
  };

  const handleMappingChange = (index: number, updates: any) => {
    const newMappings = [...mappings];
    newMappings[index] = { ...newMappings[index], ...updates };
    setMappings(newMappings);
  };

  const startImport = async () => {
    const activeMappings = mappings.filter(m => m.targetType !== 'skip');
    if (activeMappings.length === 0) {
      setError("Please map at least one folder to import.");
      return;
    }

    setIsImporting(true);
    setError(null);
    try {
      await actions.executeBookmarkImport(activeMappings);
      setStep(3);
    } catch (err: any) {
      setError(err.message || "Import failed");
    } finally {
      setIsImporting(false);
    }
  };

  if (step === 3) {
    return (
      <div className="glass glass-card text-center" style={{ padding: '3rem' }}>
        <div style={{ background: 'rgba(34, 197, 94, 0.2)', width: '64px', height: '64px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
          <Check size={32} className="text-secondary" />
        </div>
        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Import Successful!</h3>
        <p style={{ opacity: 0.6, marginBottom: '1.5rem' }}>Your bookmarks have been imported and merged into the dashboard.</p>
        <button onClick={() => window.location.reload()} className="btn btn-primary">
          View Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="glass glass-card" style={{ padding: '1.5rem', marginBottom: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <BookmarkIcon size={20} className="text-secondary" />
          Import Bookmarks
        </h3>
        <div style={{ display: 'flex', gap: '0.5rem', fontSize: '0.8rem', opacity: 0.5 }}>
          <span style={{ fontWeight: step === 1 ? 700 : 400, color: step === 1 ? 'var(--secondary)' : 'inherit' }}>1. Upload</span>
          <span>&rarr;</span>
          <span style={{ fontWeight: step === 2 ? 700 : 400, color: step === 2 ? 'var(--secondary)' : 'inherit' }}>2. Map Folders</span>
        </div>
      </div>

      {step === 1 ? (
        <div 
          onClick={() => fileInputRef.current?.click()}
          style={{ 
            border: '2px dashed var(--glass-border)', 
            borderRadius: '12px', 
            padding: '3rem', 
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.2s',
            background: isScanning ? 'rgba(255,255,255,0.05)' : 'transparent'
          }}
          onMouseOver={(e) => (e.currentTarget.style.borderColor = 'var(--secondary)')}
          onMouseOut={(e) => (e.currentTarget.style.borderColor = 'var(--glass-border)')}
        >
          {isScanning ? (
            <>
              <Loader2 className="animate-spin" size={32} style={{ margin: '0 auto 1rem' }} />
              <p>Scanning your bookmarks file...</p>
            </>
          ) : (
            <>
              <Upload size={32} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
              <p style={{ fontWeight: 500 }}>Click to upload Chrome, Edge, or Safari Bookmark HTML</p>
              <p style={{ fontSize: '0.8rem', opacity: 0.4, marginTop: '0.5rem' }}>Only .html files are supported</p>
            </>
          )}
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileSelect} 
            accept=".html" 
            style={{ display: 'none' }} 
          />
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ maxHeight: '400px', overflowY: 'auto', paddingRight: '0.5rem' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--glass-border)' }}>
                  <th style={{ padding: '0.75rem' }}>Browser Folder</th>
                  <th style={{ padding: '0.75rem' }}>Target Section</th>
                  <th style={{ padding: '0.75rem' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {mappings.map((m, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '0.75rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <FolderOpen size={16} style={{ opacity: 0.5 }} />
                        <span>{m.folderName}</span>
                        <span style={{ fontSize: '0.7rem', opacity: 0.4 }}>({m.bookmarks.length})</span>
                      </div>
                    </td>
                    <td style={{ padding: '0.75rem' }}>
                      {m.targetType === 'skip' ? (
                        <span style={{ opacity: 0.3 }}>-</span>
                      ) : m.targetType === 'existing' ? (
                        <select 
                          className="glass" 
                          value={m.targetSectionId}
                          onChange={(e) => handleMappingChange(idx, { targetSectionId: e.target.value })}
                          style={{ padding: '0.3rem', borderRadius: '4px', fontSize: '0.8rem', width: '100%' }}
                        >
                          <option value="">Select Section...</option>
                          {tabs.map(t => (
                            <optgroup key={t.id} label={t.title}>
                              {(t.sections || t.tabSections?.map((ts: any) => ts.section) || []).map((s: any) => (
                                <option key={s.id} value={s.id}>{s.title}</option>
                              ))}
                            </optgroup>
                          ))}
                        </select>
                      ) : (
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <input 
                            className="glass" 
                            placeholder="New Section Name"
                            value={m.newSectionTitle}
                            onChange={(e) => handleMappingChange(idx, { newSectionTitle: e.target.value })}
                            style={{ padding: '0.3rem', borderRadius: '4px', fontSize: '0.8rem', flex: 2 }}
                          />
                          <select 
                            className="glass" 
                            value={m.newTabId}
                            onChange={(e) => handleMappingChange(idx, { newTabId: e.target.value })}
                            style={{ padding: '0.3rem', borderRadius: '4px', fontSize: '0.8rem', flex: 1 }}
                          >
                            {tabs.map(t => <option key={t.id} value={t.id}>{t.title}</option>)}
                          </select>
                        </div>
                      )}
                    </td>
                    <td style={{ padding: '0.75rem' }}>
                      <select 
                        className="glass" 
                        value={m.targetType} 
                        onChange={(e) => handleMappingChange(idx, { targetType: e.target.value })}
                        style={{ padding: '0.3rem', borderRadius: '4px', fontSize: '0.8rem' }}
                      >
                        <option value="skip">Skip</option>
                        <option value="existing">Merge into Existing</option>
                        <option value="new">Create New Section</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--glass-border)' }}>
            <button onClick={() => setStep(1)} className="btn" style={{ fontSize: '0.8rem' }}>Back</button>
            <button 
              onClick={startImport} 
              disabled={isImporting} 
              className="btn btn-primary"
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
            >
              {isImporting ? <Loader2 size={16} className="animate-spin" /> : <Check size={16} />}
              {isImporting ? "Importing..." : "Process Import"}
            </button>
          </div>
        </div>
      )}

      {error && (
        <div style={{ marginTop: '1rem', padding: '0.75rem', borderRadius: '8px', background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', fontSize: '0.85rem' }}>
          {error}
        </div>
      )}
    </div>
  );
}
