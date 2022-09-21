def non_breaking(s):
    # Convert regular spaces to non breaking spacing
    # on the given string
    non_breaking_space = chr(160)
    return s.replace(" ", non_breaking_space)


def external_url(text, url):
    # Create a HTML element for an external url
    return '<a href="{}" target="_blank" rel="noopener noreferrer" >{}</a>'.format(url, text)
