class Consent:  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that ask consent for using the experiment data

    Relates to client component: Consent.js    
    """

    ID = "CONSENT"

    # default consent text, that can be used for multiple experiments
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

    @staticmethod
    def action(text=default_text, title='Informed consent', confirm='I agree', deny='Stop'):
        """Get data for consent action"""

        return {
            'view': Consent.ID,
            'text': text,
            'title': title,
            'confirm': confirm,
            'deny': deny
        }
