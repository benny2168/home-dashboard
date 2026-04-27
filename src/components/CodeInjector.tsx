"use client";

import { useEffect } from "react";

interface CodeInjectorProps {
  customCss?: string | null;
  customJs?: string | null;
}

export function CodeInjector({ customCss, customJs }: CodeInjectorProps) {
  useEffect(() => {
    if (customJs) {
      try {
        const script = document.createElement("script");
        script.innerHTML = customJs;
        document.body.appendChild(script);
        return () => {
          document.body.removeChild(script);
        };
      } catch (e) {
        console.error("Custom JS Injection Error:", e);
      }
    }
  }, [customJs]);

  return (
    <>
      {customCss && (
        <style id="custom-css-injector" dangerouslySetInnerHTML={{ __html: customCss }} />
      )}
    </>
  );
}
