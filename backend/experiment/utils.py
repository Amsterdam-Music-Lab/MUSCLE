import roman


def slugify(text) -> str:
    """Create a slug from given string
    
    Args:
        text (str)

    Returns:
        (str): slug
    """

    non_url_safe = ['"', '#', '$', '%', '&', '+',
                    ',', '/', ':', ';', '=', '?',
                    '@', '[', '\\', ']', '^', '`',
                    '{', '|', '}', '~', "'"]
    translate_table = {ord(char): u'' for char in non_url_safe}
    text = text.translate(translate_table)
    text = u'_'.join(text.split())
    return text.lower()


def non_breaking_spaces(s) -> str:
    """Convert regular spaces to non breaking spacing on the given string
    Args:
        s (str)

    Returns:
        (str)
    """

    non_breaking_space = chr(160)
    return s.replace(" ", non_breaking_space)


def external_url(text, url) -> str:
    """ Create a HTML element for an external url

    Args:
        text (str)
        url (str)

    Returns:
        (str): HTML element
    """

    return '<a href="{}" target="_blank" rel="noopener noreferrer" >{}</a>'.format(url, text)


def create_player_labels(num_labels, label_style='number') -> list[str]:
    """Create player labels

    Args:
        num_labels (int): Number of labels
        label_style (str): 'number', 'alphabetic', 'roman'

    Returns:
        (list[str])
    """

    return [format_label(i, label_style) for i in range(num_labels)]


def format_label(number, label_style) -> str:
    """Generate player_label for create_player_label()

    Args:
        number (int): index
        label_style (str): 'number', 'alphabetic', 'roman'

    Returns:
        (str): Player label
    """

    if label_style == 'alphabetic':
        return chr(number + 65)
    elif label_style == 'roman':
        return roman.toRoman(number+1)
    else:
        return str(number+1)
