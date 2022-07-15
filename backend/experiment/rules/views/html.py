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

    def __init__(self, html, form, style='', title='', result_id=''):
        """
        - html: HTML body
        - form: Form view
        - style: Style class, supports: STYLE_NEUTRAL, STYLE_BLUE, STYLE_PINK
        - title: Page title
        - result_id: Result id
        """
        self.title = title
        self.result_id = result_id
        self.html = html
        self.form = form
        self.style = style if style in self.STYLES else self.STYLE_NEUTRAL

    def action(self):
        """
        Serialize data for experiment action
        """
        # Create action
        action = {
            'view': HTML.ID,
            'title': self.title,
            'resultId': self.result_id,
            'style': self.style,
            'html': self.html,
            'form': self.form.action(),
        }

        return action
