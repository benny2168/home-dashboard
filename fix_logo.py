import sys
file_path = "src/components/Dashboard.tsx"
with open(file_path, "r") as f: content = f.read()

target = """                {/* Wide logo for desktop */}
                <img 
                  src={mounted && resolvedTheme === 'dark' 
                    ? (globalSettings.logoUrlDark || globalSettings.logoUrlLight || "")
                    : (globalSettings.logoUrlLight || globalSettings.logoUrlDark || "")
                  }
                  alt="System Logo"
                  className="logo-wide"
                  style={{ height: '50px', width: 'auto', objectFit: 'contain', transition: 'all 0.4s ease' }}
                />
                {/* Square logo for mobile — falls back to wide logo */}
                <img 
                  src={mounted && resolvedTheme === 'dark' 
                    ? (globalSettings.logoUrlSquareDark || globalSettings.logoUrlDark || globalSettings.logoUrlLight || "")
                    : (globalSettings.logoUrlSquareLight || globalSettings.logoUrlLight || globalSettings.logoUrlDark || "")
                  }
                  alt="System Logo"
                  className="logo-square"
                  style={{ height: '36px', width: '36px', objectFit: 'contain', borderRadius: '8px', display: 'none' }}
                />"""

replacement = """                <img 
                  src={mounted && resolvedTheme === 'dark' 
                    ? (globalSettings.logoUrlDark || globalSettings.logoUrlLight || "")
                    : (globalSettings.logoUrlLight || globalSettings.logoUrlDark || "")
                  }
                  alt="System Logo"
                  className="logo-universal"
                  style={{ height: 'var(--logo-height, 50px)', width: 'auto', maxWidth: '200px', objectFit: 'contain', transition: 'all 0.4s ease' }}
                />"""

content = content.replace(target, replacement)
with open(file_path, "w") as f: f.write(content)
print("Fixed logo width")
