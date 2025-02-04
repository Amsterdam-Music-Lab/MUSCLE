from django.utils.translation import gettext_lazy as _
from .base_action import BaseAction


class HTML(BaseAction):
    """An action that renders HTML content. See also the `HTML.tsx` component in the frontend project.

    Args:
        body (str): The HTML body content

    Examples:
        To render a simple HTML snippet with a title and a paragraph:

        >>> html_action = HTML('<h1>Hello, world!</h1><p>This is a simple HTML snippet.</p>')
    """

    view = "HTML"

    def __init__(self, body: str):
        self.body = body
