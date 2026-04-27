"use client";

import { useState, useEffect } from "react";

interface Props {
  name: string;
  defaultValue: string;
}

export function ColorSelector({ name, defaultValue }: Props) {
  const [color, setColor] = useState(defaultValue);

  useEffect(() => {
    setColor(defaultValue);
  }, [defaultValue]);

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
      <input
        type="color"
        value={color}
        onChange={(e) => setColor(e.target.value)}
        style={{
          width: "48px",
          height: "38px",
          borderRadius: "8px",
          border: "1px solid var(--glass-border)",
          background: "transparent",
          cursor: "pointer",
          padding: "2px",
        }}
      />
      <input
        type="text"
        name={name}
        value={color}
        onChange={(e) => {
          const val = e.target.value;
          if (val === "" || val.startsWith("#")) {
            setColor(val);
          }
        }}
        placeholder="#6366f1"
        style={{
          background: "rgba(0,0,0,0.25)",
          border: "1px solid var(--glass-border)",
          borderRadius: "8px",
          padding: "0.5rem 0.75rem",
          color: "inherit",
          fontFamily: "monospace",
          fontSize: "0.9rem",
          width: "100px",
        }}
      />
    </div>
  );
}
