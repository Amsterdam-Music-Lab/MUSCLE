from .base_action import BaseAction


class Info(BaseAction):
    """
    Provide data for a view that presents information using HTML to the participant, along with a customizable (link) button.

    Args:
        body (str): HTML body
        heading (str): title/heading on top
        button_label (str): label of button on bottom
        button_link (str): (optional) button link. If no link is set, clicking the button will redirect the participant to the next action.

    Example:
        ```python
        Info(
            body="<p>Here is some information</p>",
            heading="This is the heading",
            button_label="Next",
            button_link="https://example.com",
        )
        ```

    Note:
        Relates to the `Info.tsx` component in the frontend.
    """

    view = "INFO"

    def __init__(self, body, heading="", button_label=None, button_link=None):
        self.body = body
        self.heading = heading
        self.button_label = button_label
        self.button_link = button_link
