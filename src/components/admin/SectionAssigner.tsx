"use client";

import { useState } from "react";
import { Link2, Loader2 } from "lucide-react";
import { addSectionToTab } from "@/app/admin/actions";

interface Props {
  tabId: string;
  assignedIds: string[];
  allSections: any[];
}

export function SectionAssigner({ tabId, assignedIds, allSections }: Props) {
  const unassigned = allSections.filter((s) => !assignedIds.includes(s.id));
  const [selectedId, setSelectedId] = useState(unassigned[0]?.id || "");
  const [isLoading, setIsLoading] = useState(false);

  if (unassigned.length === 0) {
    return (
      <p style={{ fontSize: "0.75rem", opacity: 0.35, textAlign: "center" }}>
        All sections assigned to this tab.
      </p>
    );
  }

  const handleAssign = async () => {
    if (!selectedId) return;
    setIsLoading(true);
    await addSectionToTab(selectedId, tabId);
    setIsLoading(false);
  };

  return (
    <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
      <select
        value={selectedId}
        onChange={(e) => setSelectedId(e.target.value)}
        style={{
          flex: 1,
          background: "rgba(0,0,0,0.25)",
          border: "1px solid var(--glass-border)",
          borderRadius: "8px",
          padding: "0.45rem 0.65rem",
          color: "inherit",
          fontFamily: "inherit",
          fontSize: "0.85rem",
        }}
      >
        {unassigned.map((s) => (
          <option key={s.id} value={s.id}>
            {s.title}
          </option>
        ))}
      </select>
      <button
        onClick={handleAssign}
        disabled={isLoading || !selectedId}
        className="btn btn-primary"
        style={{ padding: "0.45rem 0.75rem", fontSize: "0.85rem", whiteSpace: "nowrap" }}
      >
        {isLoading ? <Loader2 size={14} className="animate-spin" /> : <Link2 size={14} />}
        Add
      </button>
    </div>
  );
}
