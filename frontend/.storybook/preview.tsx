import type { Preview } from "@storybook/react";
import type { ThemeName } from "../src/types/themeProvider";
import React from "react";
import { initialize, mswLoader } from "msw-storybook-addon";
import { initAudioListener } from "../src/util/audio";
import { initWebAudioListener } from "../src/util/webAudio";
import { MemoryRouter } from "react-router-dom";
import { themes } from "../src/theme/themes";
import { ThemeProvider } from "../src/theme/ThemeProvider";
import { i18n } from "@lingui/core";
import { I18nProvider } from "@lingui/react";
import { messages as messagesEn } from "@/locales/en/messages";
import { messages as messagesNl } from "@/locales/nl/messages";
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

const localeMessages = {
  en: messagesEn,
  nl: messagesNl,
};

// Global decorator to provide the theme context
const withProviders = (Story, context) => {
  const themeName = context.globals.theme as ThemeName;
  const theme = themes[themeName] ?? themes.default;

  // i18n setup
  const locale = context.globals.locale;
  const messages = localeMessages[locale] || messagesEn;
  i18n.load(locale, messages);
  i18n.activate(locale);

  return (
    <I18nProvider i18n={i18n}>
      <ThemeProvider defaultTheme={theme}>
        <MemoryRouter>
          <div className="theme-root">
            <Story />
          </div>
        </MemoryRouter>
      </ThemeProvider>
    </I18nProvider>
  );
};

const preview: Preview = {
  parameters: {
    options: {
      storySort: {
        order: ["App", "Experiments", "Modules", "Design System", "Utils"],
      },
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

    locale: {
      name: "Locale",
      description: "Internationalization locale",
      defaultValue: "en",
      toolbar: {
        icon: "globe",
        items: Object.keys(localeMessages),
      },
    },
  },
  decorators: [withProviders],
  tags: ["autodocs"],
};

export default preview;
