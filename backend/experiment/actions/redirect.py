from .base_action import BaseAction


class Redirect(BaseAction):
    """
    Redirect Action

    This action is used to redirect the user to a specified URL.

    Args:
        url (str): The URL to redirect to.

    Example:
        ```python
        redirect_action = Redirect('https://example.com')
        ```
    """

    view = "REDIRECT"

    def __init__(self, url):
        self.url = url
