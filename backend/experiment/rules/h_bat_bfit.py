from django.utils.translation import gettext_lazy as _

from .h_bat import HBat

class HBatBFIT(HBat):
    """ a class for the BFIT test, which has a different trivia section """
    ID = 'H_BAT_BFIT'

    @classmethod
    def get_trivia(cls):
        return _("Did you know... \n\nMusicians often speed up or slow down rhythms to convey a particular feeling or groove. We call this ‘expressive timing’.")
