from enum import StrEnum
from typing import Dict


class ConflictingStylesException(Exception):
    pass


class ColorScheme(StrEnum):
    """
    Enumeration of valid color schemes that can be applied to arrays of (playback) buttons

    Note:
        Color schemes are mutually exclusive. Possible values are: \n
        - BOOLEAN \n
        - BOOLEAN_NEGATIVE_FIRST \n
        - NEUTRAL \n
        - NEUTRAL_INVERTED \n
    """

    BOOLEAN = "boolean"
    BOOLEAN_NEGATIVE_FIRST = "boolean-negative-first"
    NEUTRAL = "neutral"
    NEUTRAL_INVERTED = "neutral-inverted"
    GRADIENT_7 = 'gradient-7'
    TOONTJEHOGER = 'toontjehoger'  # style with 5 different colors for buttons and links


class ButtonStyle(StrEnum):
    LARGE_GAP = "buttons-large-gap"
    LARGE_TEXT = "buttons-large-text"


class TextStyle(StrEnum):
    INVISIBLE = "invisible-text"


class FrontendStyle:
    """
    A class to manage and apply frontend styles to different elements.

    The FrontendStyle class allows setting and managing styles for various UI elements,
    with validation against predefined style options. To be used in conjunction with Playback and Question actions.

    Args:
        styles: list[str]

    Example:
        ```python
        style = FrontendStyle([ColorScheme.NEUTRAL, ButtonStyle.LARGE_GAP, TextStyle.INVISIBLE])
        ```
    """

    def __init__(self, styles=list[str]) -> None:
        for style in styles:
            self._assert_valid(style)
        self._assert_no_conflicts(styles)
        self.styles = styles

    def _assert_valid(self, style: str) -> bool:
        if style in ButtonStyle or style in ColorScheme or style in TextStyle:
            return True
        else:
            valid_styles = ", ".join(
                self._get_permissible_styles(ButtonStyle)
                + self._get_permissible_styles(ColorScheme)
                + self._get_permissible_styles(TextStyle)
            )
            raise ValueError(
                f"Invalid style: {style}. Valid styles are {valid_styles}."
            )

    def _assert_no_conflicts(self, styles: list[str]) -> bool:
        """assert that the styles array does not contain two conflicting color schemes"""
        color_schemes = list(set(styles) & set(ColorScheme))
        if len(color_schemes) <= 1:
            return True
        else:
            raise ConflictingStylesException(
                f"Cannot combine two color schemes: {color_schemes}"
            )

    def to_dict(self) -> Dict[str, str]:
        return {style: True for style in self.styles}

    def _get_permissible_styles(self, style_enum: StrEnum) -> list[str]:
        return [str(member) for member in style_enum]
