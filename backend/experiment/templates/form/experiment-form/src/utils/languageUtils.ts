import { ISO_LANGUAGES } from '../constants';

// Map of language codes to country codes for flags
// Note: This is a simplified mapping, some languages might need different country codes
export const LANGUAGE_TO_COUNTRY: { [key: string]: string } = {
  en: 'GB',
  es: 'ES',
  fr: 'FR',
  de: 'DE',
  it: 'IT',
  pt: 'PT',
  nl: 'NL',
  ru: 'RU',
  zh: 'CN',
  ja: 'JP',
  ko: 'KR',
  ar: 'SA',
  hi: 'IN',
  // Add more mappings as needed
};

export const getCountryCode = (languageCode: string): string => {
  return LANGUAGE_TO_COUNTRY[languageCode] || languageCode.toUpperCase();
};

export const getLanguageName = (languageCode: string): string => {
  return ISO_LANGUAGES[languageCode] || languageCode;
};
