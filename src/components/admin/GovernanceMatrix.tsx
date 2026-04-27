"use client";

import React from "react";
import { Users, Shield, ShieldCheck, ShieldAlert, Building2 } from "lucide-react";

interface User {
  id: string;
  name?: string | null;
  email?: string | null;
  department?: string | null;
}

interface GovernanceMatrixProps {
  itemId: string;
  users: User[];
  departments: string[];
  ownerIds: string[];
  editorIds: string[];
  viewerIds: string[];
  departmentAccess: { department: string; role: string }[];
  onUpdateUserRole: (userId: string, role: string) => Promise<void>;
  onUpdateDeptRole: (dept: string, role: string) => Promise<void>;
  onBulkDeptRole?: (dept: string, role: string) => Promise<void>;
}

export default function GovernanceMatrix({
  itemId,
  users,
  departments,
  ownerIds,
  editorIds,
  viewerIds,
  departmentAccess,
  onUpdateUserRole,
  onUpdateDeptRole,
  onBulkDeptRole
}: GovernanceMatrixProps) {
  
  const getRoleForUser = (userId: string) => {
    if (ownerIds.includes(userId)) return "owner";
    if (editorIds.includes(userId)) return "editor";
    if (viewerIds.includes(userId)) return "viewer";
    return "none";
  };

  const getRoleForDept = (dept: string) => {
    return departmentAccess.find(da => da.department === dept)?.role || "none";
  };

  const RoleBadge = ({ role }: { role: string }) => {
    switch (role) {
      case "owner": return <div title="Owner (Admin)" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text)', background: 'rgba(var(--primary-rgb), 0.1)', padding: '0.25rem 0.5rem', borderRadius: '6px', fontSize: '0.65rem', fontWeight: 800 }}><ShieldAlert size={10} /> OWNER</div>;
      case "editor": return <div title="Editor" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text)', opacity: 0.8, background: 'rgba(var(--primary-rgb), 0.1)', padding: '0.25rem 0.5rem', borderRadius: '6px', fontSize: '0.65rem', fontWeight: 800 }}><ShieldCheck size={10} /> EDITOR</div>;
      case "viewer": return <div title="Viewer" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text)', opacity: 0.6, background: 'rgba(var(--primary-rgb), 0.1)', padding: '0.25rem 0.5rem', borderRadius: '6px', fontSize: '0.65rem', fontWeight: 800 }}><Shield size={10} /> VIEWER</div>;
      default: return <div style={{ fontSize: '0.65rem', opacity: 0.3, fontWeight: 700 }}>REVOKED</div>;
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
       {departments.map(dept => {
          const deptUsers = users.filter(u => (u.department || "General") === dept);
          if (deptUsers.length === 0) return null;
          
          const deptRole = getRoleForDept(dept);

          return (
             <div key={dept} className="admin-table-wrap glass" style={{ padding: '0', borderRadius: '16px', border: '1px solid var(--glass-border)', overflow: 'auto' }}>
                <div style={{ 
                    padding: '0.75rem 1.25rem', 
                    background: 'rgba(var(--primary-rgb), 0.04)', 
                    borderBottom: '1px solid var(--glass-border)',
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between'
                }}>
                   <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <Building2 size={16} style={{ opacity: 0.4 }} />
                      <span style={{ fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{dept} Department</span>
                   </div>
                   <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <span style={{ fontSize: '0.6rem', opacity: 0.4, fontWeight: 700 }}>DEPT ACCESS:</span>
                      <select 
                        value={deptRole}
                        onChange={(e) => onUpdateDeptRole(dept, e.target.value)}
                        style={{ background: 'none', border: 'none', color: 'var(--text)', fontSize: '0.75rem', fontWeight: 800, cursor: 'pointer' }}
                      >
                         <option value="none">None</option>
                         <option value="viewer">Viewer</option>
                         <option value="editor">Editor</option>
                         <option value="owner">Owner (Admin)</option>
                      </select>
                      {onBulkDeptRole && (
                        <button 
                            onClick={() => onBulkDeptRole(dept, deptRole)}
                            style={{ padding: '0.2rem 0.6rem', borderRadius: '6px', background: 'var(--primary)', color: '#fff', fontSize: '0.65rem', fontWeight: 800, border: 'none', cursor: 'pointer' }}
                        >
                            SYNC ALL
                        </button>
                      )}
                   </div>
                </div>

                <div style={{ padding: '0.5rem' }}>
                   <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                      <tbody>
                         {deptUsers.map(user => {
                            const userRole = getRoleForUser(user.id);
                            return (
                               <tr key={user.id} style={{ borderBottom: '1px solid rgba(var(--primary-rgb), 0.05)' }}>
                                  <td style={{ padding: '0.75rem 1rem' }}>
                                     <div style={{ display: 'flex', flexDirection: 'column' }}>
                                        <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{user.name || user.email}</span>
                                        <span style={{ fontSize: '0.7rem', opacity: 0.4 }}>{user.email}</span>
                                     </div>
                                  </td>
                                  <td style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>
                                     <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '1rem' }}>
                                        <RoleBadge role={userRole} />
                                        <select 
                                          value={userRole}
                                          onChange={(e) => onUpdateUserRole(user.id, e.target.value)}
                                          style={{ background: 'none', border: '1px solid var(--glass-border)', color: 'var(--text)', borderRadius: '6px', fontSize: '0.75rem', padding: '0.2rem 0.4rem', cursor: 'pointer' }}
                                        >
                                           <option value="none">Revoke Access</option>
                                           <option value="viewer">Viewer</option>
                                           <option value="editor">Editor</option>
                                           <option value="owner">Owner (Admin)</option>
                                        </select>
                                     </div>
                                  </td>
                               </tr>
                            );
                         })}
                      </tbody>
                   </table>
                </div>
             </div>
          );
       })}
    </div>
  );
}
