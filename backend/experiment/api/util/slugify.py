def slugify(text):
    """Create a slug from given string"""
    non_url_safe = ['"', '#', '$', '%', '&', '+',
                    ',', '/', ':', ';', '=', '?',
                    '@', '[', '\\', ']', '^', '`',
                    '{', '|', '}', '~', "'"]
    translate_table = {ord(char): u'' for char in non_url_safe}
    text = text.translate(translate_table)
    text = u'_'.join(text.split())
    return text.lower()
