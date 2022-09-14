import logging
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from .views import ToontjeHoger
from .base import Base
from os.path import join
from .util.actions import combine_actions

logger = logging.getLogger(__name__)


class ExperimentData:
    # Colors
    # $teal: #39d7b8;
    # $yellow: #ffb14c;
    # $pink: #d843e2;
    # $red: #fa5577;
    # $blue: #0cc7f1;
    # $green: #00b612;
    # $indigo: #2b2bee;
    # $gray: #bdbebf;
    # $gray-900: #212529;

    def __init__(self, slug, title, description, image, color):
        self.slug = slug
        self.title = title
        self.description = description
        self.image = image
        self.color = color


class ToontjeHogerHome(Base):
    ID = 'TOONTJE_HOGER_HOME'
    TITLE = ""

    EXPERIMENT_DATA = [
        ExperimentData(slug='toontjehoger_1_mozart',
                       title="Het Mozart effect",
                       description="Helpt muziek jou met het oplossen van een korte puzzel?",
                       image="/images/experiments/toontjehoger/experiment_1.webp",
                       color="#ffb14c"
                       ),
        ExperimentData(slug='toontjehoger_3_plink',
                       title="Muziekherkenning",
                       description="Kun je met een heel kort muziekfragment een nummer herkennen?",
                       image="/images/experiments/toontjehoger/experiment_3.webp",
                       color="#fa5577"
                       ),
        ExperimentData(slug='toontjehoger_6_relative',
                       title="Relatief gehoor",
                       description="Hoor jij of de melodieën bij verschillende toonhoogte hetzelfde zijn?",
                       image="/images/experiments/toontjehoger/experiment_6.webp",
                       color="#39d7b8"
                       ),
        # Optional Experiments
        ExperimentData(slug='toontjehoger_2_first',
                       title="Het eerste luisteren",
                       description="Klink het huilen van Franse en Duitse babies verschillend? [TODO]",
                       image="/images/experiments/toontjehoger/experiment_2.webp",
                       color="#d843e2"
                       ),
        ExperimentData(slug='toontjehoger_4_absolute',
                       title="Absoluut gehoor",
                       description="Welke versie van het televisieprogramma intro heeft de juiste toonhoogte? [TODO]",
                       image="/images/experiments/toontjehoger/experiment_4.webp",
                       color="#0cc7f1"
                       ),
        ExperimentData(slug='toontjehoger_5_tempo',
                       title="Timing en tempo",
                       description="Kun je horen of welke muziekfragmenten hetzelfde tempo hebben? [TODO]",
                       image="/images/experiments/toontjehoger/experiment_5.webp",
                       color="#2b2bee"
                       ),
    ]

    @classmethod
    def first_round(cls, experiment, participant):
        """Create data for the first experiment round"""

        # Main button shows
        # - 'next experiment' when user does not have completed all experiments yet
        # - 'random experiment' when user has completed all experiments
        main_button_label = "Volgende experiment"
        main_button_url = "/{}".format(cls.EXPERIMENT_DATA[0].slug)

        # Home
        home = ToontjeHoger(
            config={
                'payoff': "Je bent muzikaler dan je denkt!",
                'intro': "Hoe snel herken jij een liedje? Heb je gevoel voor ritme en timing? Hoe goed is jouw absoluut gehoor? Doe de minigames op ToontjeHoger en ontdek meer over je eigen muzikaliteit én wat de wetenschap daarover weet.",
                'intro_read_more': "Meer informatie",
                'main_button_label': main_button_label,
                'main_button_url': main_button_url,
                'score': cls.get_score(),
                'supporters_intro': "ToontjeHoger is mede mogelijk gemaakt door:"
            },
            experiments=cls.EXPERIMENT_DATA
        ).action()

        return [
            home,
        ]

    @classmethod
    def get_score(cls):
        return 100

    def get_results(cls):
