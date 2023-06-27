from .base_action import BaseAction

class Redirect(BaseAction):
    ID = 'REDIRECT'

    def __init__(self, url):
        self.url = url
