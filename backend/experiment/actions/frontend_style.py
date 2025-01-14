from enum import Enum
from typing import Dict, Optional


class EFrontendStyle(Enum):
    """
    Enumeration of valid frontend styles that can be applied to elements.

    Example:
        ```python
        style = EFrontendStyle.PRIMARY
        ```

    Note:
        Possible values are: \n
        - EMPTY \n
        - BOOLEAN \n
        - BOOLEAN_NEGATIVE_FIRST \n
        - NEUTRAL \n
        - NEUTRAL_INVERTED \n
        - PRIMARY \n
        - SECONDARY \n
        - SUCCESS \n
        - NEGATIVE \n
        - INFO \n
        - WARNING
    """

    EMPTY = ""
    BOOLEAN = "boolean"
    BOOLEAN_NEGATIVE_FIRST = "boolean-negative-first"
    NEUTRAL = "neutral"
    NEUTRAL_INVERTED = "neutral-inverted"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    NEGATIVE = "negative"
    INFO = "info"
    WARNING = "warning"

    @staticmethod
    def is_valid(value: str) -> bool:
        return value in EFrontendStyle.__members__.values()


class FrontendStyle:
    """
    A class to manage and apply frontend styles to different elements.

    The FrontendStyle class allows setting and managing styles for various UI elements,
    with validation against predefined style options. To be used in conjunction with many of the actions like Playback and Trial.

    Args:
        root_style (EFrontendStyle): The style to apply to the root element. Defaults to EMPTY.

    Example:
        ```python
        style = FrontendStyle(EFrontendStyle.PRIMARY)
        ```
    """

    VALID_STYLES = EFrontendStyle.__members__.values()

    def __init__(self, root_style: EFrontendStyle = EFrontendStyle.EMPTY) -> None:
        if not EFrontendStyle.is_valid(root_style):
            raise ValueError(f"Invalid root style: {root_style}")

        self.styles: Dict[str, EFrontendStyle] = {"root": root_style}

    def get_style(self, element: str) -> Optional[EFrontendStyle]:
        return self.styles.get(element, None)

    def apply_style(self, element: str, style: EFrontendStyle) -> None:
        if EFrontendStyle.is_valid(style):
            self.styles[element] = style
        else:
            valid_styles = ", ".join([str(s) for s in self.VALID_STYLES])
            raise ValueError(f"Invalid style: {style}. Valid styles are {valid_styles}.")

    def to_dict(self) -> Dict[str, str]:
        return {"root": self.styles["root"].value}

    def __str__(self) -> str:
        return str(self.to_dict())

    def __json__(self) -> Dict[str, str]:
        return self.to_dict()
