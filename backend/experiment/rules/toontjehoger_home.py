import logging
import random
from .views import ToontjeHoger
from .base import Base
from .util.strings import external_url

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
                       description="Ken je dit korte muziekfragment? Noem de titel en artiest.",
                       image="/images/experiments/toontjehoger/experiment_3.webp",
                       color="#fa5577"
                       ),
        ExperimentData(slug='toontjehoger_6_relative',
                       title="Relatief gehoor",
                       description="Wanneer zijn twee getransponeerde melodieën hetzelfde?",
                       image="/images/experiments/toontjehoger/experiment_6.webp",
                       color="#39d7b8"
                       ),
        ExperimentData(slug='toontjehoger_2_preverbal',
                       title="Het eerste luisteren",
                       description="Huilen Franse en Duitse baby's hetzelfde?",
                       image="/images/experiments/toontjehoger/experiment_2.webp",
                       color="#d843e2"
                       ),
        ExperimentData(slug='toontjehoger_4_absolute',
                       title="Absoluut gehoor",
                       description="Welke versie van de televisieprogramma-intro heeft de juiste toonhoogte?",
                       image="/images/experiments/toontjehoger/experiment_4.webp",
                       color="#0cc7f1"
                       ),
        ExperimentData(slug='toontjehoger_5_tempo',
                       title="Timing en tempo",
                       description="Kan jij aan de timing van de musicus horen welk fragment het origineel is?",
                       image="/images/experiments/toontjehoger/experiment_5.webp",
                       color="#2b2bee"
                       ),
    ]

    @classmethod
    def first_round(cls, experiment, participant):
        """Create data for the first experiment round"""

        # Session history
        sessions = cls.get_sessions(participant)
        next_experiment_slug = cls.get_next_experiment_slug(sessions)

        # Score
        score = cls.get_score(sessions)
        score_label = "punten" if len(sessions) > 0 else "Nog geen punten!"
        score_class = ""
        if score < 100:
            score_class = "plastic"
        elif score < 200:
            score_class = "bronze"
        elif score < 300:
            score_class = "silver"
        elif score < 400:
            score_class = "gold"
        elif score < 500:
            score_class = "platinum"
        else:
            score_class = "diamond"

        # Main button shows
        # - 'next experiment' when user does not have completed all experiments yet
        # - 'random experiment' when user has completed all experiments
        main_button_label = "Volgende experiment" if next_experiment_slug else "Willekeurig experiment"
        main_button_url = "/{}".format(next_experiment_slug) if next_experiment_slug else random.choice([
            experiment.slug for experiment in cls.EXPERIMENT_DATA])

        # Home
        home = ToontjeHoger(
            config={
                # Home
                'payoff': "Je bent muzikaler dan je denkt!",
                'intro': "Hoe snel herken jij een liedje? Heb je gevoel voor ritme en timing? Hoe goed is jouw absoluut gehoor? Doe de minigames op ToontjeHoger en ontdek meer over je eigen muzikaliteit én wat de wetenschap daarover weet.",
                'intro_read_more': "Over ons",
                'main_button_label': main_button_label,
                'main_button_url': main_button_url,
                'score_label': score_label,
                'score': int(score),
                'score_class': score_class,
                'share_label': "Deel je score!",
                'share_message': "Ha! Ik ben muzikaler dan ik dacht - heb maar liefst {:d} punten! Speel mee met #ToontjeHoger".format(int(score)) if score > 0 else "Ha! Speel mee met #ToontjeHoger en laat je verrassen: je bent muzikaler dat je denkt!",
                'supporters_intro': "ToontjeHoger werd gemaakt door leden van muziekcognitiegroep ({}) en werd gesteund door {} en de Faculteit Geesteswetenschappen van de Universiteit van Amsterdam.".format(external_url("MCG", "https://www.mcg.uva.nl/"), external_url("KNAW Gewaardeerd!", "https://verrijkinggewaardeerd.nl/")),
                # About
                'about_title': "De ToontjeHoger website heeft als doel te laten zien dat luisteraars muzikaler zijn dan ze zelf denken én wat de wetenschap daar inmiddels over weet.",
                'about_intro': "Wil je ontdekken hoe het zit met je absoluut en relatief gehoor, je gevoel voor ritme en timing en je geheugen voor muziek? Dan zijn de ToontjeHoger mini-games vast iets voor jou!",
                'about_description': "Muziek speelt op een intrigerende manier met ons gehoor, ons geheugen, onze emoties en onze verwachtingen. Maar als luisteraar zijn we ons vaak niet bewust dat we zelf een actieve rol hebben in wat muziek zo spannend, troostend of opwindend maakt. De wetenschap heeft ontdekt dat dat luisteren zich niet afspeelt in de buitenwereld van de klinkende muziek, maar in de binnenwereld van ons hoofd en onze hersenen. Kortom: <b>iedereen is muzikaal!</b>",
                'about_streamer': "Luisteraars zijn vaak muzikaler dan ze zelf denken!",
                'about_more_title': "Meer weten?",
                'about_more_description': "Bezoek {}, {} of onze blog {}. Of lees meer over muziekcognitie in het publieksboek {}.".format(external_url("AML", "https://www.amsterdammusiclab.nl"), external_url("MCG", "https://www.mcg.uva.nl/"), external_url("Music Matters", "https://musiccognition.blogspot.com/"), external_url("Iedereen is muzikaal", "https://henkjanhoning.nl/x/iedereen-is-muzikaal.html")),
                'about_colofon_title': "Colofon",
                'about_colofon_description': "<span><b>Organisatie:</b>Zwanet Young, Henkjan Honing</span><span><b>Curatoren:</b>Mariëlle Baelemans, Fleur Bouwer, Ashley Burgoyne, Atser Damsma en Henkjan Honing</span><span><b>Advies:</b>Makiko Sadakata, Berit Janssen, en de leden van MCG</span><span><b>Realisatie:</b>Werner Helmich ({}), Berit Janssen (MUSCLE team)</span><span><b>Foto:</b>Bob Bronshoff</span>".format(external_url("SUDOX", "https://www.sudox.nl?utm_source=toontjehoger")),
                'portrait_description': "Het ToontjeHoger team (v.l.n.r.): Atser Damsma, Henkjan Honing, Zwanet Young, Mariëlle Baelemans, Fleur Bouwer, Ashley Burgoyne, Berit Janssen* en Makiko Sadakata*. (foto: Bob Bronshoff)<br><span style=\"opacity: 0.6; font-size: 0.8em;\">*Niet op de foto</span>",
                'privacy_description': "Deze website verwerkt uitsluitend geanomiseerde gegevens. Voor aanvullende informatie zie {}.".format(external_url("UvA Privacy Statement", "https://www.uva.nl/home/disclaimers/privacy.html"))
            },
            experiments=cls.EXPERIMENT_DATA
        ).action()

        return [
            home,
        ]

    @ classmethod
    def get_score(cls, sessions):
        score = 0
        for session in sessions:
            score += session.final_score
        return score

    @ classmethod
    def get_sessions(cls, participant):
        from experiment.models import Session, Experiment

        experiment_slugs = [
            experiment.slug for experiment in cls.EXPERIMENT_DATA]

        experiment_ids = Experiment.objects.filter(slug__in=experiment_slugs)

        sessions = Session.objects.filter(participant=participant,
                                          experiment_id__in=experiment_ids)
        return sessions

    @ classmethod
    def get_next_experiment_slug(cls, sessions):
        experiment_slugs = [
            experiment.slug for experiment in cls.EXPERIMENT_DATA]
        for session in sessions:
            if session.experiment.slug in experiment_slugs:
                experiment_slugs.remove(session.experiment.slug)

        if len(experiment_slugs) > 0:
            return experiment_slugs[0]

        return ''
