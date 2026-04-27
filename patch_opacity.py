#!/usr/bin/env python3
import re

with open("src/components/Dashboard.tsx", "r") as f:
    content = f.read()

# Fix Theme opacity variable bindings in Dashboard.tsx
old_glass_code = """  const isLight = theme === 'light';
  const secOpac = activeTheme.sectionOpacity ?? 0.7;
  const glsOpac = activeTheme.glassOpacity ?? 0.12;

  // Use Theme sectionOpacity and glassOpacity logically synced to the slider range
  const glassOverlayAlpha = isLight ? (secOpac * 0.8) : (secOpac * 0.08); 
  const colorTintAlpha = isLight ? 0.1 : 0.08;

  const glassBg = activeTheme.glassEffect === false ? 'var(--bg-color)' : 
      `linear-gradient(rgba(255, 255, 255, ${glassOverlayAlpha}), rgba(255, 255, 255, ${glassOverlayAlpha})), rgba(${hexToRgb(activeTheme.primaryColor)}, ${colorTintAlpha})`;"""

new_glass_code = """  const isLight = theme === 'light';
  const secOpac = activeTheme.sectionOpacity ?? 0.7;
  const glsOpac = activeTheme.glassOpacity ?? 0.12;

  // PROPERLY tie glass wash to glassOpacity!
  // Dark mode requires lower raw alpha than light mode for the same visual effect
  const glassOverlayAlpha = isLight ? (glsOpac * 0.9) : (glsOpac * 0.4); 
  
  // Tie background density to sectionOpacity
  // Let the user push the tint up to 60-80% if they want solid opaque cards
  const colorTintAlpha = isLight ? (secOpac * 0.8) : (secOpac * 0.45);

  const glassBg = activeTheme.glassEffect === false ? `rgba(${hexToRgb(activeTheme.primaryColor)}, ${colorTintAlpha})` : 
      `linear-gradient(rgba(255, 255, 255, ${glassOverlayAlpha}), rgba(255, 255, 255, ${glassOverlayAlpha})), rgba(${hexToRgb(activeTheme.primaryColor)}, ${colorTintAlpha})`;"""

content = content.replace(old_glass_code, new_glass_code)

with open("src/components/Dashboard.tsx", "w") as f:
    f.write(content)

with open("src/components/ThemeModal.tsx", "r") as f:
    content = f.read()

# Fix preview constraints in ThemeModal.tsx
old_preview_code = """  const previewSectionBg = previewIsDark ? `rgba(255,255,255,${sectionOpacity * 0.08})` : `rgba(255,255,255,${sectionOpacity})`;
  const previewBookmarkBg = previewIsDark ? `rgba(255,255,255,${sectionOpacity * 0.05})` : `rgba(255,255,255,${sectionOpacity * 0.8})`;"""

new_preview_code = """  // Create accurate preview logic mimicking the actual Dashboard rendering
  const glsOverlay = previewIsDark ? (glassOpacity * 0.4) : (glassOpacity * 0.9);
  const colorTint = previewIsDark ? (sectionOpacity * 0.45) : (sectionOpacity * 0.8);
  const rgbPrimary = "59, 130, 246"; // Base hex proxy for preview
  
  const previewSectionBg = glassEffect === false ? `rgba(${rgbPrimary}, ${colorTint})` : 
     `linear-gradient(rgba(255, 255, 255, ${glsOverlay}), rgba(255, 255, 255, ${glsOverlay})), rgba(${rgbPrimary}, ${colorTint})`;
     
  const previewBookmarkBg = previewIsDark ? `rgba(255,255,255,0.05)` : `rgba(255,255,255,0.4)`;"""

content = content.replace(old_preview_code, new_preview_code)

with open("src/components/ThemeModal.tsx", "w") as f:
    f.write(content)

print("Patch Glass/Opacity applied")
