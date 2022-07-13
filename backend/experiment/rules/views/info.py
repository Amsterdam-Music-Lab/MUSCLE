class Info:  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that shows information (HTML)

    Relates to client component: Info.js    
    """

    ID = "INFO"

    def __init__(self,body,heading="", continue_button=None):
        """ Info shows an formatted information page with an HTML body """
        
        self.body = body
        self.heading = heading
        self.continue_button = continue_button

    def action(self):
        """Get data for info action"""

        return {
            'view': Info.ID,
            'heading': self.heading,
            'body': self.body,
            'continue_button': self.continue_button,
        }
