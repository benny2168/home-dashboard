"use client";

import React, { useState, useEffect } from "react";
import { signIn } from "next-auth/react";
import { useSearchParams } from "next/navigation";
import { LogIn, ShieldCheck, LayoutGrid, Settings, Edit2, Check, LogOut, X } from "lucide-react";

const IconComponent = ({ name, size = 24, color = "currentColor" }: { name: string; size?: number, color?: string }) => {
  const icons: Record<string, any> = { LayoutGrid, ShieldCheck, Cpu: ShieldCheck, Settings, Edit2, Check, LogOut };
  const Icon = icons[name] || LayoutGrid;
  return <Icon size={size} color={color} />;
};

export function LoginForm({ logoUrl, themeColor, logoIcon, loginTheme }: { logoUrl?: string | null, themeColor: string, logoIcon?: string | null, loginTheme?: any }) {
  const searchParams = useSearchParams();
  const error = searchParams.get("error");
  const errorDescription = searchParams.get("error_description");
  const [mounted, setMounted] = useState(false);
  const [showAdminLogin, setShowAdminLogin] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  // Convert hex to rgb for glow effects
  const hexToRgb = (hex: string) => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `${r}, ${g}, ${b}`;
  };

  const themeRgb = themeColor.startsWith('#') ? hexToRgb(themeColor) : "99, 102, 241";
  
  const glassBorder = loginTheme?.darkMode ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';
  const glassBg = loginTheme?.darkMode ? `rgba(0,0,0,${loginTheme?.glassOpacity ?? 0.12})` : `rgba(255,255,255,${loginTheme?.glassOpacity ?? 0.4})`;

  return (
    <div className="login-atmospheric-container" style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      position: 'relative',
      overflow: 'hidden',
      background: loginTheme?.backgroundColor ? 'transparent' : '#050505',
      fontFamily: "'Outfit', sans-serif"
    }}>
      {/* Theme Background */}
      {loginTheme?.backgroundColor && (
         <>
            {loginTheme.backgroundColor.startsWith('http') || loginTheme.backgroundColor.startsWith('/') ? (
               <img src={loginTheme.backgroundColor} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', filter: `blur(${loginTheme.backgroundBlur ?? 0}px)`, zIndex: 0 }} />
            ) : (
               <div style={{ position: 'absolute', inset: 0, background: loginTheme.backgroundColor, zIndex: 0 }} />
            )}
            <div style={{ position: 'absolute', inset: 0, background: loginTheme.darkMode ? '#000' : '#fff', opacity: Object.hasOwn(loginTheme, 'backgroundTint') ? loginTheme.backgroundTint : 0.5, zIndex: 0 }} />
         </>
      )}

      {/* Ambient backgrounds fallback if no theme image */}
      {!loginTheme?.backgroundColor && (
         <>
            <div style={{
              position: 'absolute',
              top: '-10%',
              right: '-10%',
              width: '60%',
              height: '60%',
              background: `radial-gradient(circle, rgba(${themeRgb}, 0.15) 0%, transparent 70%)`,
              filter: 'blur(100px)',
              zIndex: 0
            }} />
            <div style={{
              position: 'absolute',
              bottom: '-10%',
              left: '-10%',
              width: '50%',
              height: '50%',
              background: 'radial-gradient(circle, rgba(236, 72, 153, 0.1) 0%, transparent 70%)',
              filter: 'blur(100px)',
              zIndex: 0
            }} />
         </>
      )}

      <div className="glass fade-in" style={{ 
        width: '100%', 
        maxWidth: '450px', 
        padding: '3.5rem 3rem', 
        borderRadius: '32px', 
        zIndex: 1, 
        textAlign: 'center',
        border: `1px solid ${glassBorder}`,
        boxShadow: `0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 40px rgba(${themeRgb}, 0.2)`,
        backdropFilter: `blur(${loginTheme?.glassEffect ? (loginTheme?.backgroundBlur || 20) : 0}px)`,
        background: glassBg,
        margin: '1rem'
      }}>
        {logoUrl ? (
          <img 
            src={logoUrl} 
            alt="Logo" 
            style={{ height: '64px', width: 'auto', margin: '0 auto 2rem auto', display: 'block', filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.1))' }} 
            onError={(e) => {
               e.currentTarget.style.display = 'none';
               // If there's a fallback sibling, display it
               if (e.currentTarget.nextElementSibling) {
                  (e.currentTarget.nextElementSibling as HTMLElement).style.display = 'flex';
               }
            }}
          />
        ) : null}
        
        <div style={{ 
          width: '80px', 
          height: '80px', 
          background: themeColor, 
          borderRadius: '24px', 
          margin: '0 auto 2rem auto', 
          display: logoUrl ? 'none' : 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          boxShadow: `0 0 40px rgba(${themeRgb}, 0.4)`
        }}>
          <IconComponent name={logoIcon || "LayoutGrid"} size={40} color="#fff" />
        </div>

        <h1 style={{ fontSize: '2.25rem', fontWeight: 800, marginBottom: '0.5rem', color: '#fff', letterSpacing: '-0.025em' }}>Dashboard</h1>
        <p style={{ fontSize: '0.9rem', color: 'rgba(255,255,255,0.4)', marginBottom: '2.5rem', lineHeight: 1.5 }}>
          Customize and consolidate links and apps in one location
        </p>

        {error && (
          <div className="glass" style={{ 
            padding: '1.25rem', 
            borderRadius: '16px', 
            background: 'rgba(239, 68, 68, 0.08)', 
            border: '1px solid rgba(239, 68, 68, 0.2)', 
            color: '#f87171', 
            fontSize: '0.9rem', 
            marginBottom: '2.5rem',
            textAlign: 'left',
            lineHeight: 1.5
          }}>
            <div style={{ fontWeight: 700, marginBottom: '0.25rem' }}>Authentication Error</div>
            {error === "AccessDenied" ? (
              <>
                <div style={{ opacity: 0.9 }}>You do not have permission to access this portal.</div>
                {errorDescription && <div style={{ marginTop: '0.5rem', opacity: 0.6, fontSize: '0.75rem' }}>{errorDescription}</div>}
              </>
            ) : "There was a problem signing you in. Please try again."}
          </div>
        )}

        <button 
          onClick={() => signIn("microsoft-entra-id", { callbackUrl: "/" })}
          className="btn"
          style={{ 
            width: '100%', 
            padding: '1.1rem', 
            borderRadius: '16px', 
            fontSize: '1rem', 
            fontWeight: 700, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            gap: '1.25rem',
            transition: 'all 0.3s ease',
            marginBottom: '2rem',
            background: '#fff',
            color: '#000',
            border: 'none',
            boxShadow: '0 4px 15px rgba(0,0,0,0.2)'
          }}
        >
          <svg width="22" height="22" viewBox="0 0 23 23">
            <path d="M11.5 0H0V11.5H11.5V0Z" fill="#f25022"/>
            <path d="M23 0H11.5V11.5H23V0Z" fill="#7fbb00"/>
            <path d="M11.5 11.5H0V23H11.5V11.5Z" fill="#00a1f1"/>
            <path d="M23 11.5H11.5V23H23V11.5Z" fill="#ffbb00"/>
          </svg>
          Sign in with Microsoft
        </button>

        {/* Admin login link */}
        <button
          onClick={() => setShowAdminLogin(true)}
          style={{
            background: 'none',
            border: 'none',
            color: 'rgba(255,255,255,0.25)',
            fontSize: '0.75rem',
            cursor: 'pointer',
            textDecoration: 'underline',
            fontFamily: 'inherit',
            transition: 'color 0.2s'
          }}
          onMouseEnter={(e) => (e.currentTarget.style.color = 'rgba(255,255,255,0.5)')}
          onMouseLeave={(e) => (e.currentTarget.style.color = 'rgba(255,255,255,0.25)')}
        >
          Admin Login
        </button>

        <div style={{ marginTop: '2.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', opacity: 0.2 }}>
           <ShieldCheck size={14} />
           <span style={{ fontSize: '0.65rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.15em' }}>Secure Authentication</span>
        </div>
      </div>

      {/* Admin Login Modal */}
      {showAdminLogin && (
        <div 
          className="modal-overlay"
          onClick={(e) => e.target === e.currentTarget && setShowAdminLogin(false)}
          style={{ 
            position: 'fixed', 
            inset: 0, 
            background: 'rgba(0,0,0,0.8)', 
            backdropFilter: 'blur(10px)', 
            zIndex: 1000, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            padding: '1rem'
          }}
        >
          <div className="glass modal-content fade-in" style={{ 
            width: '100%', 
            maxWidth: '400px', 
            padding: '2.5rem 2rem', 
            borderRadius: '24px', 
            border: '1px solid rgba(255,255,255,0.1)',
            background: 'rgba(20,20,25,0.95)',
            backdropFilter: 'blur(20px)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <ShieldCheck size={20} style={{ color: themeColor }} />
                <span style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff' }}>Admin Login</span>
              </div>
              <button 
                onClick={() => setShowAdminLogin(false)} 
                style={{ background: 'none', border: 'none', color: 'rgba(255,255,255,0.4)', cursor: 'pointer', padding: '0.25rem' }}
              >
                <X size={20} />
              </button>
            </div>

            <form 
              onSubmit={async (e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                const username = formData.get("username") as string;
                const password = formData.get("password") as string;
                await signIn("credentials", { username, password, callbackUrl: "/" });
              }}
              style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}
            >
              <input 
                name="username"
                type="text" 
                placeholder="Username" 
                autoComplete="username"
                style={{ 
                  width: '100%',
                  padding: '1rem 1.25rem', 
                  borderRadius: '14px', 
                  background: 'rgba(255,255,255,0.05)', 
                  border: '1px solid rgba(255,255,255,0.1)',
                  color: '#fff',
                  fontSize: '0.95rem',
                  outline: 'none',
                  transition: 'all 0.3s ease',
                  boxSizing: 'border-box'
                }}
              />
              <input 
                name="password"
                type="password" 
                placeholder="Password" 
                autoComplete="current-password"
                style={{ 
                  width: '100%',
                  padding: '1rem 1.25rem', 
                  borderRadius: '14px', 
                  background: 'rgba(255,255,255,0.05)', 
                  border: '1px solid rgba(255,255,255,0.1)',
                  color: '#fff',
                  fontSize: '0.95rem',
                  outline: 'none',
                  transition: 'all 0.3s ease',
                  boxSizing: 'border-box'
                }}
              />
              <button 
                type="submit"
                style={{ 
                  padding: '1rem', 
                  borderRadius: '14px', 
                  background: themeColor, 
                  color: '#fff',
                  fontWeight: 700,
                  fontSize: '0.95rem',
                  border: 'none',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  boxShadow: `0 4px 15px rgba(${themeRgb}, 0.3)`
                }}
              >
                Sign In
              </button>
            </form>
          </div>
        </div>
      )}

      <style jsx global>{`
        .fade-in {
          animation: fadeIn 1s cubic-bezier(0.4, 0, 0.2, 1);
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        input:focus {
          border-color: ${themeColor} !important;
          background: rgba(255,255,255,0.08) !important;
          box-shadow: 0 0 20px rgba(${themeRgb}, 0.15);
        }
        button:hover {
          filter: brightness(1.1);
          transform: translateY(-2px);
        }
        input::placeholder {
          color: rgba(255,255,255,0.3);
        }
      `}</style>
    </div>
  );
}
