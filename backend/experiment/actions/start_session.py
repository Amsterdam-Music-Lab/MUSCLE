from .base_action import BaseAction

class StartSession(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a StartSession view
    - This is a required view in each experiment that handles the creation of a new session
    - It should only be called after consent has been given by the participant
    - As this view is more a technical step/necessity it doesn't have any additional data beside the view id

    Relates to client component: StartSession.js    
    """

    ID = "START_SESSION"