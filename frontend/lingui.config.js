import { defineConfig } from "@lingui/cli";
import { locales, defaultLocale } from "./src/i18n";

export default defineConfig({
  sourceLocale: defaultLocale,
  locales: Object.keys(locales),
  catalogs: [
    {
      path: "<rootDir>/src/locales/{locale}/messages",
      include: ["src", "config"],
    },
  ],
});
