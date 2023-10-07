from .base_action import BaseAction

class Info(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that shows information (HTML)

    Relates to client component: Info.js    
    """

    ID = "INFO"

    def __init__(self, body, heading="", button_label=None, button_link=None):
        """
        Info shows an formatted information page with an HTML body
        body: html body
        heading: title/heading on top
        button_label: label of button on bottom
        button_link: (optional) button link. If no link is set, 'onNext' is called
        """
        
        self.body = body
        self.heading = heading
        self.button_label = button_label
        self.button_link = button_link
