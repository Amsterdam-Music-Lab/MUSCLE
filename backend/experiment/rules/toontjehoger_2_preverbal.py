import logging
from django.template.loader import render_to_string

from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Trial, Explainer, Step, Score, Final, StartSession, Playlist, Info, HTML
from experiment.actions.form import ButtonArrayQuestion, ChoiceQuestion, Form
from experiment.actions.playback import Playback
from experiment.actions.styles import STYLE_NEUTRAL
from .base import Base
from os.path import join
from experiment.actions.utils import combine_actions
from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHoger2Preverbal(Base):
    ID = 'TOONTJE_HOGER_2_PREVERBAL'
    TITLE = ""
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Het eerste luisteren",
            steps=[
                Step(
                    "Je krijgt drie spectrogrammen te zien met de vraag: welk geluid is van een mens?"),
                Step(
                    "Daarvoor eerst nog wat uitleg van wat een spectrogram is, natuurlijk."),
                Step(
                    "Tenslotte krijg je twee geluiden te horen met de vraag: welke baby is in Frankrijk geboren?"),
            ],
            button_label="Start"

        ).action(step_numbers=True)

        # 2 Spectrogram information
        spectrogram_info = cls.get_spectrogram_info()

        # 3. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session.
        start_session = StartSession.action()

        return [
            explainer,
            spectrogram_info,
            playlist,
            start_session
        ]

    @classmethod
    def get_spectrogram_info(cls):
        image_url = "/images/experiments/toontjehoger/spectrogram_info_nl.webp"
        description = "Een spectrogram is een visuele weergave van geluid, waarin je kan zien hoe een geluid verandert over de tijd. Hoe witter, hoe meer energie op die frequentie."
        body = '<div class="center"><img src="{}"></div><p>{}</p>'.format(
            image_url, description)

        # Return answer info view
        info = Info(
            body=body,
            heading="Wat is een spectrogram?",
            button_label="Volgende",
        ).action()
        return info

    @classmethod
    def next_round(cls, session, request_session=None):
        """Get action data for the next round"""

        rounds_passed = session.rounds_passed()

        # Round 1
        if rounds_passed == 0:
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return cls.get_round1(session)

        # Round 2
        if rounds_passed == 1:
            return combine_actions(*cls.get_score(session, rounds_passed), *cls.get_round1_playback(session), *cls.get_round2(round, session))

        # Final
        return combine_actions(*cls.get_final_round(session))

    @classmethod
    def get_score(cls, session, rounds_passed):
        # Feedback
        last_result = session.last_result()
        feedback = ""
        if not last_result:
            logger.error("No last result")
            feedback = "Er is een fout opgetreden"
        else:
            if rounds_passed == 1:
                appendix = "Op het volgende scherm kun je de geluiden beluisteren."
                if last_result.score == cls.SCORE_CORRECT:
                    feedback = "Dat is correct! Spectrogram C is inderdaad van een mens. " + appendix
                else:
                    feedback = "Helaas! Je antwoord was onjuist. Het geluid van spectrogram C is van een mens. " + appendix
            elif rounds_passed == 2:
                if last_result.score == cls.SCORE_CORRECT:
                    feedback = "Dat is correct! Geluid A is inderdaad de Franse baby."
                else:
                    feedback = "Helaas! Geluid A is de Franse baby."

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback).action()
        return [score]

    @classmethod
    def get_round1(cls, session):
        # Question
        key = 'expected_spectrogram'
        question = ButtonArrayQuestion(
            question="Welk spectrogram toont het geluid van een mens?",
            key=key,
            choices={
                'A': 'A',
                'B': 'B',
                'C': 'C',
            },
            view='BUTTON_ARRAY',
            submits=True,
            result_id=prepare_result(
                key, session, expected_response="C"
            )
        )
        form = Form([question])

        image_trial = Trial(
            html=HTML(
            body='<img src="{}" style="height:calc(100% - 260px);max-height:326px;max-width: 100%;"/>'.format(
                "/images/experiments/toontjehoger/preverbal_1.webp")),
            feedback_form=form,
            title=cls.TITLE,
        ).action()

        return [image_trial]

    @classmethod
    def get_round1_playback(cls, session):
        # Get sections
        sectionA = session.section_from_any_song(
            filter_by={'tag': 'a', 'group': '1'})
        if not sectionA:
            raise Exception(
                "Error: could not find section A for round 1")

        sectionB = session.section_from_any_song(
            filter_by={'tag': 'b', 'group': '1'})
        if not sectionB:
            raise Exception(
                "Error: could not find section B for round 1")

        sectionC = session.section_from_any_song(
            filter_by={'tag': 'c', 'group': '1'})
        if not sectionB:
            raise Exception(
                "Error: could not find section C for round 1")

        # Player
        play_config = {
            'label_style': 'ALPHABETIC',
            'spectrograms': ["/images/experiments/toontjehoger/spectrogram-trumpet.webp", "/images/experiments/toontjehoger/spectrogram-whale.webp", "/images/experiments/toontjehoger/spectrogram-human.webp"],
            'spectrogram_labels': ['Trompet', 'Walvis', 'Mens'],
        }
        playback = Playback(
            [sectionA, sectionB, sectionC], player_type=Playback.TYPE_SPECTROGRAM, play_config=play_config)

        trial = Trial(
            playback=playback,
            feedback_form=None,
            title=cls.TITLE,
            style='primary-form'
        ).action()
        return [trial]

    @classmethod
    def get_round2(cls, round, session):

        # Get sections
        # French
        sectionA = session.section_from_any_song(
            filter_by={'tag': 'a', 'group': '2'})
        if not sectionA:
            raise Exception(
                "Error: could not find section A for round 2")
        # German
        sectionB = session.section_from_any_song(
            filter_by={'tag': 'b', 'group': '2'})
        if not sectionB:
            raise Exception(
                "Error: could not find section B for round 2")

        # Player
        play_config = {
            'label_style': 'ALPHABETIC',
            'spectrograms': ["/images/experiments/toontjehoger/spectrogram-baby-french.webp", "/images/experiments/toontjehoger/spectrogram-baby-german.webp"]
        }
        playback = Playback(
            [sectionA, sectionB], player_type=Playback.TYPE_SPECTROGRAM, play_config=play_config)

        # Question
        key = 'baby'
        question = ChoiceQuestion(
            question="Welke baby is in Frankrijk geboren?",
            key=key,
            choices={
                "A": "A",
                "B": "B",
            },
            view='BUTTON_ARRAY',
            submits=True,
            result_id=prepare_result(key, session, expected_response="A"),
            style=STYLE_NEUTRAL
        )
        form = Form([question])

        trial = Trial(
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
        score = cls.get_score(session, session.rounds_passed())

        # Final
        final_text = "Goed gedaan! Je hebt beide vragen correct beantwoord!" if session.final_score >= 2 * \
            cls.SCORE_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        ).action()

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment2.html'))
        info = Info(
            body=body,
            heading="Het eerste luisteren",
            button_label="Terug naar ToontjeHoger",
            button_link="/toontjehoger"
        ).action()

        return [*score, final, info]
