from .base_action import BaseAction

class Consent(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that ask consent for using the experiment data

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
    
    def __init__(self, text=default_text, title='Informed consent', confirm='I agree', deny='Stop'):
        self.text = text
        self.title = title
        self.confirm = confirm
        self.deny = deny
