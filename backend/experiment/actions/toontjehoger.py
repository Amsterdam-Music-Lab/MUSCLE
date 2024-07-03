from .base_action import BaseAction


class ToontjeHoger(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that shows the ToontjeHoger homepage

    Relates to client component: ToontjeHoger.js
    """

    ID = "TOONTJEHOGER"

    def __init__(self, config, blocks=[]):
        """
        ToontjeHoger shows the ToontjeHoger homepage

        config: Object containing texts and other configuration
            - payoff
            - intro
            - main_button_label
            - main_button_url
            - score_label
            - supporters_intro
        blocks: A list of ExperimentData objects
        """
        self.config = config
        self.blocks = [vars(i) for i in self.blocks]
