"use client";

import { useState } from "react";
import { Palette, CheckCircle2, Plus, Trash2, Edit2, Upload, X } from "lucide-react";
import { ColorSelector } from "./ColorSelector";
import * as actions from "@/app/admin/actions";

interface Theme {
  id: string;
  name: string;
  logoUrl: string | null;
  dashboardTitle?: string;
  logoIcon?: string | null;
  primaryColor: string;
  backgroundColor: string | null;
  darkMode: boolean;
  glassEffect: boolean;
  isActive: boolean;
}

interface Props {
  initialThemes: Theme[];
}

export function ThemeManager({ initialThemes }: Props) {
  const [themes, setThemes] = useState(initialThemes);
  const [editingTheme, setEditingTheme] = useState<Theme | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  const activeTheme = themes.find((t) => t.isActive);

  const handleEdit = (theme: Theme) => {
    setEditingTheme(theme);
    setIsCreating(false);
  };

  const handleCancel = () => {
    setEditingTheme(null);
    setIsCreating(false);
  };

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2rem" }}>
      {/* Left: Theme List */}
      <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <h3 style={{ fontSize: "0.75rem", fontWeight: 600, opacity: 0.7, textTransform: "uppercase", letterSpacing: "0.05em" }}>
          Saved Themes
        </h3>

        {themes.map((theme) => (
          <div
            key={theme.id}
            className="glass"
            style={{
              padding: "1.25rem",
              borderRadius: "14px",
              border: theme.isActive ? `2px solid var(--primary)` : "1px solid var(--glass-border)",
              display: "flex",
              flexDirection: "column",
              gap: "1rem",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                <div
                  style={{
                    width: "28px",
                    height: "28px",
                    borderRadius: "8px",
                    background: theme.primaryColor,
                    border: "2px solid rgba(255,255,255,0.2)",
                    flexShrink: 0,
                  }}
                />
                <div>
                  <p style={{ fontWeight: 600, margin: 0 }}>{theme.name}</p>
                  <p style={{ fontSize: "0.75rem", opacity: 0.5, margin: 0 }}>
                    {theme.darkMode ? "Dark" : "Light"} · {theme.glassEffect ? "Glass" : "Solid"}
                  </p>
                </div>
              </div>
              <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
                <button
                  onClick={() => handleEdit(theme)}
                  className="btn"
                  style={{ padding: "0.4rem", background: "rgba(255,255,255,0.05)" }}
                >
                  <Edit2 size={14} />
                </button>
                {theme.isActive && (
                  <span style={{ fontSize: "0.7rem", padding: "0.2rem 0.6rem", background: "rgba(99,102,241,0.15)", color: "var(--primary)", borderRadius: "99px", fontWeight: 600 }}>
                    ACTIVE
                  </span>
                )}
              </div>
            </div>

            <div style={{ display: "flex", gap: "0.5rem" }}>
              {!theme.isActive && (
                <button
                  onClick={async () => {
                    await actions.activateTheme(theme.id);
                  }}
                  className="btn btn-primary"
                  style={{ flex: 1, justifyContent: "center" }}
                >
                  <CheckCircle2 size={15} />
                  Activate
                </button>
              )}
              <button
                onClick={async () => {
                  if (confirm("Delete this theme?")) {
                    await actions.deleteTheme(theme.id);
                  }
                }}
                className="btn"
                style={{ background: "rgba(239, 68, 68, 0.1)", color: "#ef4444", border: "none" }}
                disabled={theme.isActive}
              >
                <Trash2 size={15} />
              </button>
            </div>
          </div>
        ))}

        <button
          onClick={() => {
            setIsCreating(true);
            setEditingTheme(null);
          }}
          className="btn glass"
          style={{ width: "100%", justifyContent: "center", border: "1px dashed var(--glass-border)", padding: "1rem" }}
        >
          <Plus size={18} />
          Create New Theme
        </button>
      </div>

      {/* Right: Form Area */}
      <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        {(editingTheme || isCreating) ? (
          <div className="glass glass-card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
              <h3 style={{ fontSize: "1rem", fontWeight: 600, display: "flex", alignItems: "center", gap: "0.5rem" }}>
                {isCreating ? <Plus size={18} /> : <Edit2 size={18} />}
                {isCreating ? "Create New Theme" : `Editing Theme: ${editingTheme?.name}`}
              </h3>
              <button onClick={handleCancel} className="btn" style={{ padding: "0.4rem" }}>
                <X size={16} />
              </button>
            </div>

            <form
              onSubmit={async (e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                if (isCreating) {
                  await actions.createTheme(formData);
                } else if (editingTheme) {
                  await actions.updateTheme(editingTheme.id, formData);
                }
                handleCancel();
              }}
              style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}
            >
              <label style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
                <span style={{ fontSize: "0.8rem", opacity: 0.6, fontWeight: 500 }}>Theme Name *</span>
                <input
                  name="name"
                  defaultValue={editingTheme?.name || ""}
                  required
                  placeholder="e.g. Minimalist Dark"
                  className="glass"
                  style={{ padding: "0.6rem 0.75rem", borderRadius: "8px", border: "1px solid var(--glass-border)", color: "inherit", width: "100%" }}
                />
              </label>

              <label style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
                <span style={{ fontSize: "0.8rem", opacity: 0.6, fontWeight: 500 }}>Logo Image</span>
                <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                  {editingTheme?.logoUrl && (
                    <img 
                      src={editingTheme.logoUrl} 
                      alt="Logo" 
                      style={{ height: '40px', width: '40px', objectFit: 'contain', background: 'rgba(255,255,255,0.05)', borderRadius: '4px' }} 
                    />
                  )}
                  <div style={{ position: 'relative', flex: 1 }}>
                    <input
                      type="file"
                      name="logo"
                      accept="image/*"
                      className="glass"
                      style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', cursor: 'pointer', fontSize: '0.8rem' }}
                    />
                    <input type="hidden" name="currentLogoUrl" value={editingTheme?.logoUrl || ""} />
                  </div>
                </div>
              </label>

              <label style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
                <span style={{ fontSize: "0.8rem", opacity: 0.6, fontWeight: 500 }}>Primary Color (Accent)</span>
                <ColorSelector name="primaryColor" defaultValue={editingTheme?.primaryColor || "#6366f1"} />
              </label>

              <label style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
                <span style={{ fontSize: "0.8rem", opacity: 0.6, fontWeight: 500 }}>Background Color (Gradient/Solid)</span>
                <ColorSelector name="backgroundColor" defaultValue={editingTheme?.backgroundColor || (editingTheme?.darkMode ? "#000000" : "#f0f9ff")} />
              </label>

              <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '12px', border: '1px solid var(--glass-border)', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <span style={{ fontSize: "0.75rem", fontWeight: 700, opacity: 0.5, textTransform: "uppercase" }}>Branding</span>
                
                <label style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
                  <span style={{ fontSize: "0.8rem", opacity: 0.6, fontWeight: 500 }}>Dashboard Title</span>
                  <input
                    name="dashboardTitle"
                    defaultValue={editingTheme?.dashboardTitle || "Dashboard"}
                    placeholder="e.g. My Workspace"
                    className="glass"
                    style={{ padding: "0.6rem 0.75rem", borderRadius: "8px", border: "1px solid var(--glass-border)", color: "inherit", width: "100%" }}
                  />
                </label>

                <label style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
                  <span style={{ fontSize: "0.8rem", opacity: 0.6, fontWeight: 500 }}>Logo Icon (Lucide Name)</span>
                  <input
                    name="logoIcon"
                    defaultValue={editingTheme?.logoIcon || ""}
                    placeholder="e.g. LayoutGrid, Zap, etc."
                    className="glass"
                    style={{ padding: "0.6rem 0.75rem", borderRadius: "8px", border: "1px solid var(--glass-border)", color: "inherit", width: "100%" }}
                  />
                </label>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                <span style={{ fontSize: "0.8rem", opacity: 0.6, fontWeight: 500 }}>Options</span>
                
                <label style={{ display: "flex", alignItems: "center", gap: "0.75rem", cursor: "pointer" }}>
                  <input
                    type="checkbox"
                    name="darkMode"
                    defaultChecked={editingTheme?.darkMode ?? true}
                    className="glass"
                  />
                  <span style={{ fontSize: "0.9rem" }}>Dark Mode</span>
                </label>

                <label style={{ display: "flex", alignItems: "center", gap: "0.75rem", cursor: "pointer" }}>
                  <input
                    type="checkbox"
                    name="glassEffect"
                    defaultChecked={editingTheme?.glassEffect ?? true}
                    className="glass"
                  />
                  <span style={{ fontSize: "0.9rem" }}>Glass Effect</span>
                </label>

                {!isCreating && editingTheme && (
                  <label style={{ display: "flex", alignItems: "center", gap: "0.75rem", cursor: "pointer" }}>
                    <input
                      type="checkbox"
                      name="isActive"
                      defaultChecked={editingTheme.isActive}
                      className="glass"
                    />
                    <span style={{ fontSize: "0.9rem" }}>Is Active</span>
                  </label>
                )}
              </div>

              <button type="submit" className="btn btn-primary" style={{ justifyContent: "center", marginTop: "1rem" }}>
                {isCreating ? <Plus size={16} /> : <CheckCircle2 size={16} />}
                {isCreating ? "Create Theme" : "Save Changes"}
              </button>
            </form>
          </div>
        ) : (
          <div className="glass" style={{ padding: "3rem", borderRadius: "12px", textAlign: "center", opacity: 0.4, display: "flex", flexDirection: "column", alignItems: "center", gap: "1rem" }}>
            <Palette size={48} />
            <p>Select a theme to edit or create a new one.</p>
          </div>
        )}
      </div>
    </div>
  );
}
