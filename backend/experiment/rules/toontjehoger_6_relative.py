import logging
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from random import randint
from experiment.models import Section
from .views import Trial, Explainer, Step, Score, Final, StartSession, Playlist, Info
from .views.form import ChoiceQuestion, Form, DropdownQuestion
from .views.playback import Playback
from .base import Base
from os.path import join
from .util.actions import combine_actions

logger = logging.getLogger(__name__)


class ToontjeHoger6Relative(Base):
    ID = 'TOONTJE_HOGER_6_RELATIVE'
    TITLE = ""
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    @classmethod
    def first_round(cls, experiment, participant):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Relatief Gehoor",
            steps=[
                Step("In deze mini-game kan je testen hoe goed jouw relatieve gehoor is! Relatief gehoor is het vermogen om een melodie te herkennen, ongeacht of die nu wat hoger of lager in toonhoogte wordt afgespeeld."),
                # Empty step adds some spacing between steps to improve readability
                Step(""),
                Step(
                    "Je krijgt twee melodieën te horen, verschillend in toonhoogte.", number=1),
                Step("Luister goed, want je kunt ze maar één keer afspelen!", number=2),
                Step("Aan jou de taak om te ontrafelen of deze melodieën hetzelfde zijn, ongeacht de toonhoogte! ", number=3),
            ],
            button_label="Start"

        ).action(step_numbers=False)

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
            return cls.get_round(session)

        # Round 2
        if rounds_passed == 1:
            return combine_actions(*cls.get_score(session), *cls.get_round(session))

        # Final
        return combine_actions(*cls.get_final_round(session))

    @classmethod
    def get_score(cls, session):
        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config).action()
        return [score]

    @classmethod
    def get_round(cls, session):

        # Config
        # -----------------
        section1 = session.section_from_unused_song(
            filter_by={'group': '2', 'tag': 'original'})
        if section1 == None:
            raise Exception("Error: could not find section1 for round")
        section2 = session.section_from_unused_song(
            filter_by={'artist': section1.artist, 'name': section1.name, 'tag': 'variation'})
        if section2 == None:
            section2 = section1
            # TODO: FIX
            # raise Exception("Error: could not find section2 for round")

        correct_section = section1 if randint(0, 1) == 1 else section2
        expected_response = correct_section.pk
        result_pk = cls.prepare_result(
            session, section=correct_section, expected_response=expected_response)

        # Question
        question = ChoiceQuestion(
            question="Waren deze twee melodieën hetzelfde?",
            key='same_melodie',
            choices={
                "YES": _('YES'),
                "NO": _('NO'),
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])

        # Player
        play_config = {
            'label_style': 'ALPHABETIC',
            'play_once': True,
        }
        playback = Playback(
            [section1, section2], player_type=Playback.TYPE_MULTIPLAYER, play_config=play_config)

        # Trial
        trial_config = {
            'style': 'boolean blue-players',
        }

        trial = Trial(
            config=trial_config,
            playback=playback,
            feedback_form=form,
            title=cls.TITLE,
        ).action()
        return [trial]

    @classmethod
    def calculate_score(cls, result, data, form_element):
        return cls.SCORE_CORRECT if result.expected_response == result.given_response else cls.SCORE_WRONG

    @classmethod
    def get_final_round(cls, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = cls.get_score(session)

        # Final
        final_text = "Goed gedaan, jouw relatief gehoor is uitstekend!" if session.final_score >= 2 * \
            cls.SCORE_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=cls.rank(session),
            button={'text': 'Wat hebben we getest?'}
        ).action()

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment6.html'))
        info = Info(
            body=body,
            heading="Relatief gehoor",
            button_label="Terug naar ToontjeHoger",
            button_link="https://www.amsterdammusiclab.nl"
        ).action()

        return [*score, final, info]
