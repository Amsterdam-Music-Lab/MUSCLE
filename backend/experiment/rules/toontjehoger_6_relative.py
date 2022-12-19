import logging
from django.template.loader import render_to_string
from os.path import join
from .toontjehoger_1_mozart import toontjehoger_ranks
from .views import Trial, Explainer, Step, Score, Final, StartSession, Playlist, Info
from .views.form import ChoiceQuestion, Form
from .views.playback import Playback
from .base import Base
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
                Step("In dit experiment kun je testen hoe goed jouw relatieve gehoor is! Relatief gehoor is het vermogen om een melodie te herkennen, ongeacht of deze nu wat hoger of lager in toonhoogte wordt afgespeeld."),
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
            return cls.get_round(rounds_passed, session)

        # Round 2
        if rounds_passed == 1:
            return combine_actions(*cls.get_score(session), *cls.get_round(round, session))

        # Final
        return combine_actions(*cls.get_final_round(session))

    @classmethod
    def get_score(cls, session):
        # Feedback
        last_result = session.last_result()

        if not last_result:
            logger.error("No last result")
            feedback = "Er is een fout opgetreden"
        else:
            if last_result.score == cls.SCORE_CORRECT:
                feedback = "Dat is correct! De melodieën in de muziekfragmenten zijn inderdaad verschillend."
            else:
                feedback = "Helaas! De melodieën in de muziekfragmenten zijn toch echt verschillend."

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback).action()
        return [score]

    @classmethod
    def get_round(cls, round, session):

        # Config
        # -----------------
        # section 1 is always section 'a'
        section1 = session.section_from_any_song(
            filter_by={'tag': 'a'})
        if section1 == None:
            raise Exception(
                "Error: could not find section1 for round {}".format(round))

        # Get correct tag for round 0 or 1
        tag = 'b' if round == 0 else 'c'
        section2 = session.section_from_any_song(
            filter_by={'tag': tag})
        if section2 == None:
            raise Exception(
                "Error: could not find section2 for round {}".format(round))

        # Fragments A,B,C are all different, so answer is always NO
        expected_response = "NO"

        # Question
        question = ChoiceQuestion(
            question="Zijn deze twee melodieën hetzelfde?",
            key='same_melodie',
            choices={
                "YES": "Ja",
                "NO": "Nee",
            },
            view='BUTTON_ARRAY',
            submits=True
        )
        question.prepare_result(
            session, section=section1, expected_response=expected_response
        )
        form = Form([question])

        # Player
        play_config = {
            'label_style': 'CUSTOM',
            'labels': ['A', 'B' if round == 0 else 'C'],
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
    def calculate_score(cls, result, data):
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
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        ).action()

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment6.html'))
        info = Info(
            body=body,
            heading="Relatief gehoor",
            button_label="Terug naar ToontjeHoger",
            button_link="/toontjehoger"
        ).action()

        return [*score, final, info]
