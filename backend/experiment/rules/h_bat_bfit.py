from django.utils.translation import gettext_lazy as _

from .h_bat import HBat

class HBatBFIT(HBat):
    """ a class for the BFIT test, which has a different trivia section """
    ID = 'H_BAT_BFIT'

    def get_trivia(self):
        return _("Musicians often speed up or slow down rhythms to convey a particular feeling or groove. We call this ‘expressive timing’.")
