import type {Preview} from "@storybook/react"
import type { ThemeName } from "../src/types/themeProvider";
import React from "react";
import { initialize, mswLoader } from "msw-storybook-addon";
import { initAudioListener } from "../src/util/audio";
import { initWebAudioListener } from "../src/util/webAudio";
import { MemoryRouter } from "react-router-dom";
import { themes } from "../src/theme/themes";
import { ThemeProvider } from "../src/theme/ThemeProvider";
import "../public/vendor/bootstrap/bootstrap.min.css";
import "../src/index.scss";

// Init audio listener
initAudioListener();
initWebAudioListener();

// Initialize MSW
initialize({
  serviceWorker: {
    url: "./mockServiceWorker.js",
  },

  // Silence unhandled request warnings
  onUnhandledRequest: "bypass",
});

// Global decorator to provide the theme context
const withThemeProvider = (Story, context) => {
  const themeName = context.globals.theme as ThemeName;
  const theme = themes[themeName] ?? themes.default;

  return (
    <ThemeProvider defaultTheme={theme}>
      <MemoryRouter>
        <div className="theme-root">
          <Story />
        </div>
      </MemoryRouter>
    </ThemeProvider>
  );
};

const preview: Preview = {
  parameters: {
    options: {
      storySort: {
        order: ['App', 'Experiments', 'Modules', 'Design System', 'Utils']
      }
    },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    
  },

  // Provide the MSW addon loader globally
  loaders: [mswLoader],

  // Allow selecting the theme in the Storybook UI
  globalTypes: {
    theme: {
      name: "Theme",
      description: "Global theme for components",
      defaultValue: "mcgLight",
      toolbar: {
        icon: "paintbrush",
        items: Object.keys(themes),
        showName: true,
      },
    },
  },
  decorators: [withThemeProvider],
  tags: ["autodocs"],
};

export default preview;
