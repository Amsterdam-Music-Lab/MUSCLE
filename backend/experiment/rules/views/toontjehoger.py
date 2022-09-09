class ToontjeHoger:  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that shows the ToontjeHoger homepage

    Relates to client component: ToontjeHoger.js
    """

    ID = "TOONTJEHOGER"

    def __init__(self,payoff="", slogan = "", experiments = []):
        """
        ToontjeHoger shows the ToontjeHoger homepage
        """
        self.payoff = payoff
        self.slogan = slogan
        self.experiments = experiments

    def action(self):
        """Get data for ToontjeHoger action"""

        return {
            'view': ToontjeHoger.ID,
            'payoff': self.payoff,
            'slogan': self.slogan,
            'experiments': self.experiments,
        }
