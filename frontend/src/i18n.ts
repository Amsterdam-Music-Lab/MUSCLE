import { i18n } from "@lingui/core";
import { detect, fromNavigator } from "@lingui/detect-locale";

export const locales = {
  en: "English",
  nl: "Nederlands",
};

export const defaultLocale = "nl";

export function detectLocale() {
  const locale = detect(fromNavigator(), () => defaultLocale);
  if (locale.startsWith("nl")) {
    return "nl";
  }
  return "en";
}

/**
 * We do a dynamic import of just the catalog that we need
 * @param locale any locale string
 */
export async function dynamicActivate(locale: string) {
  const { messages } = await import(`./locales/${locale}/messages.ts`);
  i18n.load(locale, messages);
  i18n.activate(locale);
}
