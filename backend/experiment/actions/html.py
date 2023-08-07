from django.utils.translation import gettext_lazy as _
from .base_action import BaseAction


class HTML(BaseAction):  # pylint: disable=too-few-public-methods
    """
    A custom view that handles a custom HTML question
    Relates to client component: HTML.js    
    """

    ID = 'HTML'

    def __init__(self, body):
        """
        - body: HTML body
        """
        self.body = body
