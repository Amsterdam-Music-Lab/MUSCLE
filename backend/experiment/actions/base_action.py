class BaseAction(object):
    ID = 'BASE'

    def __init__(self):
        pass

    def action(self):
        self.view = self.ID
        return self.__dict__
