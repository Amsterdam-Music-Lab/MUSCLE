/**
 * Renders a template string. Templates are of the form "Here is a {{key}}."
 * The {{key}} will be replaced by the value of the key in the data object.
 * The template string can contain any number of {{key}} placeholders.
 * The key must be a string and the value can be a string or a number.
 * 
 * @param template The template string
 * @param data An object with keys and values
 * @returns A formatted string
 */
export function renderTemplate(
  template: string,
  data: Record<string, string | number>
): string {
  return template.replace(/{{\s*(\w+)\s*}}/g, (_, key) => {
    const value = data[key];
    return value !== undefined ? String(value) : '';
  });
}
