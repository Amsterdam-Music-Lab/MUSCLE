from .base_action import BaseAction
from django.template.loader import render_to_string
from django.template import Template, Context
from django_markup.markup import formatter

def get_render_format(url):
    """
    Detect markdown file by file extention 
    """
    url_length = len(url)
    if url[(url_length-2):url_length].lower() == 'md':
        return 'MARKDOWN'
    return 'HTML'

class Consent(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that ask consent for using the experiment data
    - text: Uploaded file via experiment.consent (fileField)
    - title: The title to be displayed
    - confirm: The text on the confirm button
    - deny: The text on the deny button
    - url:  If no text is provided the url will be used to load a template (HTML or MARKDOWN)            
    - render_format: (autodetected from the file extention)
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
        # Determine which text to use        
        if text!='':
            # Uploaded consent via file field: experiment.consent (High priority)
            with text.open('r') as f:
                dry_text = f.read()
            render_format = get_render_format(text.url)        
        elif url!='':
            # Template file via url (Low priority)
            dry_text = render_to_string(url)
            render_format = get_render_format(url)        
        else:
            # use default text
            dry_text = self.default_text
        # render text fot the consent component
        if render_format == 'HTML':
            template = Template(dry_text)
            context = Context()
            self.text = template.render(context)
        if render_format == 'MARKDOWN':
            self.text = formatter(dry_text, filter_name='markdown')
        self.title = title
        self.confirm = confirm
        self.deny = deny
        self.render_format = render_format
