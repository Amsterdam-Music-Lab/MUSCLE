import logging
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from random import randint
from .views import  Trial, Explainer, Step, Score, Final, StartSession, Playlist, Info
from .views.form import ChoiceQuestion, RadiosQuestion, Form, DropdownQuestion, RadiosQuestion
from .views.playback import Playback
from .base import Base
from os.path import join
from .util.actions import combine_actions
from pprint import pprint

logger = logging.getLogger(__name__)


class ToontjeHoger3Plink(Base):
    ID = 'TOONTJE_HOGER_3_PLINK'
    TITLE = _("Toontje Hoger")
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Uitleg",
            steps=[
                Step(_("Luister naar een heel kort muziekfragment.")),
                Step(
                    _("Ken je het nummer? Noem de juiste artiest en titel.")),
                Step(
                    _("Weet je het niet? Beantwoord dan extra vragen over tijdsperiode en emotie."))
            ],
            button_label=_("Start")

        ).action(step_numbers=True)

        # 2. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 3. Start session.
        start_session = StartSession.action()

        return [
            explainer,
            playlist,
            start_session
        ]

    @classmethod
    def next_round(cls, session, request_session=None):
        """Get action data for the next round"""


        rounds_passed = session.rounds_passed()

        # Round 1
        if rounds_passed == 0:
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return cls.get_main_question(session) + cls.get_optional_question1(session) + cls.get_optional_question2(session)

        # Round 2-6
        if rounds_passed <= 5:
            return combine_actions(*cls.get_score(session), *cls.get_main_question(session))

        # Final
        return combine_actions(*cls.get_final_round(session))

    @classmethod
    def get_score(cls, session):
        # Return score view
        config = {'show_total_score': True, 'show_section': True}
        score = Score(session, config=config).action()

        return [score]

    @classmethod
    def get_main_question(cls, session):

        # Config
        # -----------------

        # Get all song sections
        all_sections = session.all_sections()
        choices = {}
        for section in all_sections:
            label = section.song_label()
            choices[section.pk] = label

        # Get section to recognize
        section = session.section_from_unused_song()
        if section == None:
            raise Exception("Error: could not find section")

        expected_response = section.pk
        result_pk = cls.prepare_result(
            session, section=section, expected_response=expected_response)

        # Main question
        # --------------------

        # Question
        question = DropdownQuestion(
            question=_('Noem de artiest en de titel van het nummer'),
            key='recognize',
            choices=choices,
            result_id=result_pk,
            submits=False
        )
        button = ChoiceQuestion(
            key='dont_know',
            choices={
                'skip': _("Ik weet het niet"),
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question,button])

        # Player
        play_config = {'auto_play': True}
        playback = Playback(
            [section], player_type=Playback.TYPE_BUTTON, play_config=play_config)

        # Trial
        trial_config = {}
        trial = Trial(
            config=trial_config,
            playback=playback,
            feedback_form=form,
            title=cls.TITLE,
        ).action()

        return [trial]

    @classmethod
    def get_optional_question1(cls, session):

        # Config
        # -----------------
        
        # Question
        periods = ["60's", "70's", "80's", "90's", "00's", "10's", "20's"]
        period_choices = {}
        for period in periods:
            period_choices[period.replace("'", "")] = period.capitalize()

        question = RadiosQuestion(
            question=_('Wanneer is het nummer uitgebracht?'),
            key='time_period',
            choices=period_choices,
            submits=False
        )
        form = Form([question])

        # Trial question 1
        trial = Trial(
            feedback_form=form,
            title=cls.TITLE,
        ).action()

        return [trial]

    @classmethod
    def get_optional_question2(cls, session):

        # Question
        emotions = ['vrolijk', 'droevig', 'boosheid', 'angst', 'tederheid']
        emotion_choices = {}
        for emotion in emotions:
            emotion_choices[emotion] = emotion.capitalize()

        question = RadiosQuestion(
            question=_('Welke emotie past bij dit nummer?'),
            key='time_period',
            choices=emotion_choices,
            submits=True
        )
        form = Form([question])

        # Trial
        trial = Trial(
            feedback_form=form,
            title=cls.TITLE,
        ).action()

        return [trial]

    @classmethod
    def calculate_score(cls, result, form_element, data):
        return cls.SCORE_CORRECT if result.expected_response == result.given_response else cls.SCORE_WRONG

    @classmethod
    def get_final_round(cls, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = cls.get_score(session)

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment3.html'))
        info = Info(body=body, heading=_("Muziekherkenning"),
                    continue_button=_("Volgende")).action()

        # Final
        final_text = _("Goed gedaan, jouw muziekherkenning is uitstekend!") if session.final_score >= 2 * \
            cls.SCORE_CORRECT else _("Wellicht nog een poging wagen? Er is ruimte voor verbetering.")
        final = Final(
            session=session,
            final_text=final_text,
            rank=cls.rank(session),
            button={'link': 'https://www.amsterdammusiclab.nl',
                    'text': 'Terug naar ToontjeHoger'}
        ).action()

        return [*score, info, final]
