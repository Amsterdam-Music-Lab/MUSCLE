import { defineConfig } from "@lingui/cli";
import { locales, defaultLocale } from "./src/i18n";

export default defineConfig({
  sourceLocale: defaultLocale,
  locales: Object.keys(locales),
  catalogs: [
    {
      path: "src/locales/{locale}/messages",
      include: ["src/components/**", "src/config/**"],
    },
  ],
});
