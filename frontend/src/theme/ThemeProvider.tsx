// src/theme/ThemeProvider.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { themeToCSSVariables } from './themeToCssVariables';
import { themes, Theme, ThemeName} from './themes';

// TODO move to utils?
function omit<T extends object, K extends keyof T>(
  obj: T,
  keys: K[]
): Omit<T, K> {
  return Object.fromEntries(
    Object.entries(obj).filter(([key]) => !keys.includes(key as K))
  ) as Omit<T, K>;
}


interface ThemeContextType {
  theme: Theme;
  setThemeByName: (name: ThemeName) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within a ThemeProvider');
  return ctx;
};

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({
  useTheme,
  children 
}) => {
  const defaultTheme = useTheme || themes.default;
  const [theme, setTheme] = useState<Theme>(defaultTheme);

  const setThemeByName = (name: ThemeName) => setTheme(themes[name]);

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute('data-theme', theme.name);
    root.setAttribute('data-theme-type', theme.type);

    // Set CSS variables
    const excludedKeys = ['name', 'fontUrl', 'backgroundUrl', 'useGradients', 'type'];
    const cssVars = themeToCSSVariables(omit(theme, excludedKeys));
    for (const [key, value] of Object.entries(cssVars)) {
      if(!excludedKeys.includes(key)){
        root.style.setProperty(key, value);
      }
    };

    // --background-url has to be defined as "url(...)"
    if(theme.backgroundUrl) {
      root.style.setProperty('--background-url', `url(${theme.backgroundUrl})`);
    }

    // Set the font URL
    if (theme.fontUrl) {
      const existing = document.querySelector(`link[data-theme-font]`);
      if (existing) existing.remove();
  
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = theme.fontUrl;
      link.setAttribute('data-theme-font', 'true');
      document.head.appendChild(link);
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setThemeByName }}>
      {children}
    </ThemeContext.Provider>
  );
};
