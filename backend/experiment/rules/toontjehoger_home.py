import logging
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from .views import ToontjeHoger
from .base import Base
from os.path import join
from .util.actions import combine_actions

logger = logging.getLogger(__name__)

class ToontjeHogerHome(Base):
    ID = 'TOONTJE_HOGER_HOME'
    TITLE = ""

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        home = ToontjeHoger(
            payoff="Je bent muzikaler dan je denkt!",
            slogan="Hoe snel herken jij een liedje? Heb je gevoel voor ritme en timing? Hoe goed is jouw absoluut gehoor? Doe de minigames op ToontjeHoger en ontdek meer over je eigen muzikaliteit én wat de wetenschap daarover weet",
            experiments=[]
        ).action()


        # Info page
        # body = render_to_string(
        #     join('info', 'toontjehoger', 'experiment6.html'))
        # info = Info(
        #     body=body,
        #     heading="Relatief gehoor",
        #     button_label="Terug naar ToontjeHoger",
        #     button_link="https://www.amsterdammusiclab.nl"
        # ).action()

        return [
            home,
        ]
    