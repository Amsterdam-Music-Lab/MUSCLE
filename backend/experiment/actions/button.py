from typing import Optional, TypedDict

from .base_action import BaseAction
from theme.models import ThemeConfig

valid_colors = ThemeConfig().valid_colors()

class ButtonAction(TypedDict):
    label: str
    color: str
    link: Optional[str]


class Button(BaseAction):
    """A button object to be used for ButtonArrayQuestions, as PlayButton, or a skip / submit buttons

    Args:
        label: a (translatable) label of the button
        color: a color field from ThemeConfig


    """

    def __init__(self, label: str, color: str = "colorPrimary", link: str = ''):
        self.label = label
        self.color = self.validate_color(color)
        self.link = link

    def validate_color(self, color: str):
        if color not in valid_colors:
            raise ValueError(f"{color} is not a valid color value")
        return color
