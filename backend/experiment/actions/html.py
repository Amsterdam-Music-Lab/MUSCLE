from django.utils.translation import gettext_lazy as _


class HTML(object):  # pylint: disable=too-few-public-methods
    """
    A custom view that handles a custom HTML question
    Relates to client component: HTML.js    
    """

    ID = 'HTML'

    STYLE_NEUTRAL = 'neutral'
    STYLE_BLUE = 'blue'
    STYLE_PINK = 'pink'

    STYLES = [STYLE_NEUTRAL, STYLE_BLUE, STYLE_PINK]

    def __init__(self, body):
        """
        - body: HTML body
        """
        self.body = body

    def action(self):
        """
        Serialize data for experiment action
        """
        # Create action
        action = {
            'view': HTML.ID,
            'body': self.body,
        }

        return action
