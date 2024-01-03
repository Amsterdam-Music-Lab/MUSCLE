class FrontendStyle:
    EMPTY = ''
    BOOLEAN = 'boolean'
    NEUTRAL = 'neutral'
    BOOLEAN_INVERTED = 'boolean-inverted'
    NEUTRAL_INVERTED = 'neutral-inverted'

    VALID_STYLES = {EMPTY, BOOLEAN, NEUTRAL, BOOLEAN_INVERTED, NEUTRAL_INVERTED}

    """
    Initialize the FrontendStyle with a root style, and optionally nested styles.
    :param root_style: The style name for the root element.
    :param nested_styles: A dictionary where keys are element identifiers and values are style names.
    """
    def __init__(self, root_style = EMPTY, **nested_styles):

        if root_style not in self.VALID_STYLES:
            raise ValueError(f"Invalid root style: {root_style}")

        self.styles = {'root': root_style}

        for element, nested_style in nested_styles.items():
            if isinstance(nested_style, FrontendStyle):
                self.styles[element] = nested_style
            else:
                raise ValueError(f"Nested styles must be of type FrontendStyle, got {type(nested_style)} for '{element}'")


    def get_style(self, element):
        """
        Get the style for a specific element.
        :param element: The element identifier for which to get the style.
        :return: The style name for the given element.
        """
        return self.styles.get(element, None)

    def apply_style(self, element, style):
        """
        Apply a specific style to an element after validating the style.
        :param element: The element identifier to apply the style to.
        :param style: The style name to apply.
        """
        if style in self.VALID_STYLES:
            self.styles[element] = style
        else:
            raise ValueError(f"Invalid style: {style}. Valid styles are: {', '.join(self.VALID_STYLES)}")

    def to_dict(self):
        serialized_styles = {'root': self.styles['root']}
        for element, style in self.styles.items():
            if element != 'root':
                serialized_styles[element] = style.to_dict() if isinstance(style, FrontendStyle) else style
        return serialized_styles
