from enum import Enum


class EFrontendStyle(Enum):
    EMPTY = ''
    BOOLEAN = 'boolean'
    BOOLEAN_NEGATIVE_FIRST = 'boolean-negative-first'
    NEUTRAL = 'neutral'
    NEUTRAL_INVERTED = 'neutral-inverted'
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    SUCCESS = 'success'
    NEGATIVE = 'negative'
    INFO = 'info'
    WARNING = 'warning'

    @staticmethod
    def is_valid(value):
        return value in EFrontendStyle.__members__.values()


class FrontendStyle:

    VALID_STYLES = EFrontendStyle.__members__.values()

    """
    Initialize the FrontendStyle with a root style, and optionally nested styles.
    :param root_style: The style name for the root element.
    """
    def __init__(self, root_style: EFrontendStyle = EFrontendStyle.EMPTY):

        if not EFrontendStyle.is_valid(root_style):
            raise ValueError(f"Invalid root style: {root_style}")

        self.styles = { 'root': root_style }

    def to_dict(self) -> dict:
        serialized_styles = { 'root': self.styles['root'].value }

        return serialized_styles
    
    def __str__(self):
        return str(self.to_dict())
    
    def __json__(self):
        return self.to_dict()
