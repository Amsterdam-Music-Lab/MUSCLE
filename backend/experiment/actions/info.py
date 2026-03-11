from typing import Optional

from .base_action import BaseAction
from .button import Button

class Info(BaseAction):
    """
    Provide data for a view that presents information using HTML to the participant, along with a customizable (link) button.

    Args:
        body (str): HTML body
        heading (str): title/heading on top
        button (Button): properties of the button shown under the body

    Example:
        ```python
        Info(
            body="<p>Here is some information</p>",
            heading="This is the heading",
            button=Button("Next", "colorPrimary", "https://example.com"),
        )
        ```

    Note:
        Relates to the `Info.tsx` component in the frontend.
    """

    view = "INFO"

    def __init__(self, body, heading="", button: Optional[Button] = None):
        self.body = body
        self.heading = heading
        self.button = button
