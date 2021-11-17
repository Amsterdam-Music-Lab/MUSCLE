
class Redirect(object):
    """
    Provide data for a redirect view

    Relates to client component: Redirect.js 
    """

    ID = 'REDIRECT'

    @staticmethod
    def action(slug):
        """Get data for redirect action"""
        action = {
            'view': Redirect.ID,
            'slug': slug
        }
        return action