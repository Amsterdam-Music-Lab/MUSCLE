const toKebabCase = (str: string): string =>
  str.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();

export const themeToCSSVariables = (
  theme: Record<string, any>,
  prefix = ''
): Record<string, string> => {
  const result: Record<string, string> = {};

  for (const [key, value] of Object.entries(theme)) {
    const kebabKey = toKebabCase(key);
    const varKey = prefix ? `${prefix}-${kebabKey}` : kebabKey;

    if (typeof value === 'object' && value !== null) {
      Object.assign(result, themeToCSSVariables(value, varKey));
    } else {
      result[`--${varKey}`] = value.toString();
    }
  }

  return result;
};
