from .base_action import BaseAction


class Redirect(BaseAction):
    """
    Redirect Action

    This action is used to redirect the user to a specified URL.

    Attributes:
        ID (str): Identifier for the action, set to 'REDIRECT'.
        url (str): The URL to which the redirection should occur.

    Args:
        url (str): The URL to redirect to.

    Example:
        redirect_action = Redirect('https://example.com')
    """

    ID = "REDIRECT"

    def __init__(self, url):
        self.url = url
