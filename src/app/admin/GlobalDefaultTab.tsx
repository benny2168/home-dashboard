"use client";

import { useState } from "react";
import { updateGlobalDefaultTab } from "./actions";

export function GlobalDefaultTab({ allTabs, currentDefaultTabId }: { allTabs: { id: string; title: string }[]; currentDefaultTabId: string | null }) {
  const [value, setValue] = useState(currentDefaultTabId || "");

  const handleChange = async (tabId: string) => {
    setValue(tabId);
    await updateGlobalDefaultTab(tabId || null);
  };

  return (
    <select 
      value={value}
      onChange={(e) => handleChange(e.target.value)}
      className="glass"
      style={{ padding: '0.4rem 0.6rem', borderRadius: '8px', fontSize: '0.8rem', cursor: 'pointer', minWidth: '140px' }}
    >
      <option value="">First Available</option>
      {allTabs.map(t => <option key={t.id} value={t.id}>{t.title}</option>)}
    </select>
  );
}
