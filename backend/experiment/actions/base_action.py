from .frontend_style import FrontendStyle


class BaseAction(object):
    """base class for the experiment actions.
    Actions are used to configure components to be rendered on the frontend.    
    """

    ID = 'BASE'
    style = None

    def __init__(self, style: FrontendStyle = None):
        self.style = style
        pass

    def action(self) -> dict:
        """The action that can be sent to the frontend
    
        Returns:
            action_dict (dict): Frontend component configuration        
        """

        action_dict = self.__dict__
        action_dict['view'] = self.ID

        # we may have already converted the style object to a dictionary, e.g., after copying an Action object
        if self.style is not None and type(self.style) is not dict:
            action_dict['style'] = self.style.to_dict()

        return action_dict
