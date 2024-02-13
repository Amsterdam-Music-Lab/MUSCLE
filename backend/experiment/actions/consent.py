from .base_action import BaseAction
from django.template.loader import render_to_string
from django.template import Template, Context
from django_markup.markup import formatter

class Consent(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that ask consent for using the experiment data
    - text: Has priority over 'url'
    - title: The title to be displayed
    - confirm: The text on the confirm button
    - deny: The text on the deny button
    - url:  If no text is provided the url will be used to load a template (HTML or MARKDOWN)            
    - render_format: (autodetected when reading from a file)
        'HTML': (default) Allowed tags: html, django template language
        'MARKDOWN': Allowed tags: Markdown language

    Relates to client component: Consent.js    
    """

    # default consent text, that can be used for multiple experiments
    ID = 'CONSENT'

    default_text = "Lorem ipsum dolor sit amet, nec te atqui scribentur. Diam \
                molestie posidonium te sit, ea sea expetenda suscipiantur \
                contentiones, vix ex maiorum denique! Lorem ipsum dolor sit \
                amet, nec te atqui scribentur. Diam molestie posidonium te sit, \
                ea sea expetenda suscipiantur contentiones, vix ex maiorum \
                denique! Lorem ipsum dolor sit amet, nec te atqui scribentur. \
                Diam molestie posidonium te sit, ea sea expetenda suscipiantur \
                contentiones, vix ex maiorum denique! Lorem ipsum dolor sit \
                amet, nec te atqui scribentur. Diam molestie posidonium te sit, \
                ea sea expetenda suscipiantur contentiones."
    
    def __init__(self, text, title='Informed consent', confirm='I agree', deny='Stop', url='', render_format='HTML'):
        if text!='':
            dry_text = text
        elif url!='':
            dry_text = render_to_string(url)
            url_length = len(url)
            if url[(url_length-2):url_length] == 'md':
                render_format = 'MARKDOWN'
        else:
            dry_text = self.default_text
        if render_format == 'HTML':
            template = Template(dry_text)
            context = Context()
            self.text = template.render(context)
        if render_format == 'MARKDOWN':
            self.text = formatter(dry_text, filter_name='markdown')
        self.title = title
        self.confirm = confirm
        self.deny = deny
