
def serialize(actions):
    ''' Serialize an array of actions '''
    if isinstance(actions, list):
        return [a.action() for a in actions]
    return actions.action()


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


def non_breaking_spaces(s):
    # Convert regular spaces to non breaking spacing
    # on the given string
    non_breaking_space = chr(160)
    return s.replace(" ", non_breaking_space)


def external_url(text, url):
    # Create a HTML element for an external url
    return '<a href="{}" target="_blank" rel="noopener noreferrer" >{}</a>'.format(url, text)
