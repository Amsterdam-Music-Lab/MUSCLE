/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Theme, ThemeName } from "@/types/themeProvider";
import type { ReactNode } from "react";
import { createContext, useContext, useEffect, useState } from "react";
import { omit } from "@/util/object";
import { themeToCSSVariables } from "./themeToCssVariables";
import { themes } from "./themes";

type ThemeProp = keyof Theme;

interface ThemeContextType {
  theme: Theme;
  setThemeByName: (name: ThemeName) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

/**
 * The useTheme hook that returns the current theme.
 */
export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within a ThemeProvider");
  return ctx;
};

interface ThemeProviderProps {
  /** Name of the default theme to use. Defaults to themes.default */
  defaultTheme?: Theme;

  /** Children */
  children: ReactNode;
}

/**
 * Provides the application with a theme
 */
export function ThemeProvider({ defaultTheme, children }: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(defaultTheme ?? themes.default);
  const setThemeByName = (name: ThemeName) => setTheme(themes[name]);

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute("data-theme", theme.name);
    root.setAttribute("data-theme-type", theme.type);

    // Set CSS variables
    const excludedKeys = [
      "name",
      "fontUrl",
      "backgroundUrl",
      "useGradients",
      "type",
    ] as Array<ThemeProp>;
    const cssVars = themeToCSSVariables(omit(theme, excludedKeys));
    for (const [key, value] of Object.entries(cssVars)) {
      if (!excludedKeys.includes(key as ThemeProp)) {
        root.style.setProperty(key, value);
      }
    }

    // --background-url has to be defined as "url(...)"
    if (theme.backgroundUrl) {
      root.style.setProperty("--background-url", `url(${theme.backgroundUrl})`);
    }

    // Set the font URL
    if (theme.fontUrl) {
      const existing = document.querySelector(`link[data-theme-font]`);
      if (existing) existing.remove();

      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = theme.fontUrl;
      link.setAttribute("data-theme-font", "true");
      document.head.appendChild(link);
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setThemeByName }}>
      {children}
    </ThemeContext.Provider>
  );
}
