// src/theme/ThemeProvider.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { themeToCSSVariables } from './themeToCssVariables';
import { themes, Theme, ThemeName} from './themes';

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

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>(themes.default);

  const setThemeByName = (name: ThemeName) => {
    setTheme(themes[name]);
  };

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute('data-theme', theme.name);
    const cssVars = themeToCSSVariables(theme);
    for (const [key, value] of Object.entries(cssVars)) {
      if(key != 'name') {
        root.style.setProperty(key, value);
      }
    };
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setThemeByName }}>
      {children}
    </ThemeContext.Provider>
  );
};
