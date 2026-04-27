import re

with open("src/components/IconPicker.tsx", "r") as f:
    content = f.read()

# 1. Update activeSource init
content = content.replace(
    'const [activeSource, setActiveSource] = useState<"catalog" | "extended" | "custom">("catalog");',
    'const [activeSource, setActiveSource] = useState<"catalog" | "brands" | "extended" | "custom">("catalog");'
)

# 2. Update the button mapper
content = content.replace(
    '{(["catalog", "extended", "custom"] as const).map(src => (',
    '{(["catalog", "brands", "extended", "custom"] as const).map(src => ('
)

# 3. Update the button labels 
content = content.replace(
    '{src === "catalog" ? "Logos" : src === "extended" ? "Universal" : "Custom"}',
    '{src === "catalog" ? "Logos" : src === "brands" ? "Brands" : src === "extended" ? "Universal" : "Custom"}'
)

# 4. Integrate the Brandfetch Picker component exactly like IconifyPicker
brandfetch_render = """
      {activeSource === "brands" && (
         <BrandfetchPicker setIcon={setIcon} currentIcon={currentIcon} />
      )}
"""
content = content.replace(
    '{activeSource === "extended" && (',
    brandfetch_render + '      {activeSource === "extended" && ('
)

# 5. Add BrandfetchPicker component at the end of the file
brandfetch_component = """

const BrandfetchPicker = ({ setIcon, currentIcon }: any) => {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);
    const [searching, setSearching] = useState(false);

    const search = async () => {
        if (!query) return;
        setSearching(true);
        try {
            const res = await fetch(`https://api.brandfetch.io/v2/search/${encodeURIComponent(query)}`);
            const data = await res.json();
            if (Array.isArray(data)) {
               setResults(data);
            } else {
               setResults([]);
            }
        } catch (e) {
            console.error(e);
            setResults([]);
        }
        setSearching(false);
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div className="glass" style={{ padding: '0.75rem', borderRadius: '12px', background: 'rgba(0,0,0,0.1)' }}>
                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.75rem' }}>
                    <input 
                        className="glass" 
                        value={query} 
                        onChange={(e) => setQuery(e.target.value)} 
                        onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), search())}
                        placeholder="Search millions of brands (e.g. Google, Nike, Apple)..." 
                        style={{ flex: 1, padding: '0.6rem', fontSize: '0.8rem', borderRadius: '8px' }} 
                    />
                    <button type="button" onClick={(e) => { e.preventDefault(); search(); }} className="btn btn-primary" style={{ padding: '0.6rem 1rem', borderRadius: '8px', fontSize: '0.8rem' }}>
                        {searching ? "..." : "Search"}
                    </button>
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', maxHeight: '180px', overflowY: 'auto' }}>
                    {results.map((brand, idx) => {
                        if (!brand.icon) return null;
                        const iconUrl = brand.icon;
                        return (
                          <button 
                              key={`${brand.domain}-${idx}`}
                              type="button"
                              onClick={() => setIcon(iconUrl)}
                              className="glass"
                              title={brand.name}
                              style={{ 
                                  padding: '8px', borderRadius: '10px', cursor: 'pointer', transition: 'all 0.2s', 
                                  border: currentIcon === iconUrl ? '2px solid var(--primary)' : '1px solid transparent',
                                  background: currentIcon === iconUrl ? 'rgba(var(--primary-rgb), 0.2)' : 'rgba(255,255,255,0.05)',
                                  display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem',
                                  width: '56px'
                              }}
                          >
                              <img src={iconUrl} style={{ width: '32px', height: '32px', objectFit: 'contain' }} alt={brand.name} />
                              <span style={{ fontSize: '0.5rem', opacity: 0.6, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', width: '100%' }}>{brand.name}</span>
                          </button>
                        );
                    })}
                    {!results.length && !searching && <p style={{ fontSize: '0.75rem', opacity: 0.3, width: '100%', textAlign: 'center', padding: '1rem' }}>Enter a brand name to fetch its official logo.</p>}
                </div>
            </div>
        </div>
    );
};
"""

content += brandfetch_component

with open("src/components/IconPicker.tsx", "w") as f:
    f.write(content)
