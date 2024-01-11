from .frontend_style import FrontendStyle

class BaseAction(object):
    ID = 'BASE'

    def __init__(self, style = FrontendStyle()):
        self.style = style
        pass

    def action(self):
        action_dict = self.__dict__
        action_dict['view'] = self.ID
        action_dict['style'] = self.style.to_dict()

        return action_dict
