from django.utils.translation import gettext_lazy as _
from .base_action import BaseAction


class HTML(BaseAction):
    """An action that renders HTML content.

    Attributes:
        ID (str): Identifier for the HTML action.
        body (str): The HTML body content.
    """

    ID = "HTML"

    def __init__(self, body: str):
        """Initialize an HTML action.

        Args:
            body (str): The HTML body content.
        """
        self.body = body
