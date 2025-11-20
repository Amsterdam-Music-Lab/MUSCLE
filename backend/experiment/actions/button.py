from typing import Optional, TypedDict

class ButtonAction(TypedDict):
    label: str
    color: str
    link: Optional[str]

class Button(object):
    """A button object to be used for ButtonArrayQuestions, as PlayButton, or a skip / submit buttons

    Args:
        label: a (translatable) label of the button
        color: a color field from ThemeConfig


    """

    def __init__(self, label: str, color: str = "colorPrimary", link: str = ''):
        self.label = label
        self.color = color
        self.link = link

    def action(self) -> ButtonAction:
        return {'label': self.label, 'color': self.color, 'link': self.link or None}