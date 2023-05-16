class Redirect(object):
    ID = 'REDIRECT'

    def __init__(self, url):
        self.url = url

    def action(self):
        return {
            'view': self.ID,
            'url': self.url
        }
