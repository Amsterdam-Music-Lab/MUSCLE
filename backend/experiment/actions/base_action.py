from .frontend_style import FrontendStyle


class BaseAction(object):
    ID = 'BASE'
    style = None

    def __init__(self, style: FrontendStyle = None):
        self.style = style
        pass

    def action(self):
        action_dict = self.__dict__
        action_dict['view'] = self.ID

        if self.style is not None:
            action_dict['style'] = self.style.to_dict()

        return action_dict
