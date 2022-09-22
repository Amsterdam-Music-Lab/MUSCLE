import logging
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from random import randint
from .views import Trial, Explainer, Step, Score, Final, StartSession, Playlist, Info, HTML
from .views.form import ButtonArrayQuestion, ChoiceQuestion, Form, DropdownQuestion
from .views.playback import Playback
from .base import Base
from os.path import join
from .util.actions import combine_actions

logger = logging.getLogger(__name__)


class ToontjeHoger2Preverbal(Base):
    ID = 'TOONTJE_HOGER_2_PREVERBAL'
    TITLE = ""
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    @classmethod
    def first_round(cls, experiment, participant):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Het eerste luisteren",
            steps=[
                Step(
                    "Je krijgt drie spectrogrammen* te zien met de vraag: welk geluid is van een mens?", number=1),
                Step(
                    "Daarna krijg je twee geluiden te horen met de vraag: welke baby is in Frankrijk geboren?", number=2),
                Step(""),
                Step("* Een spectrogram is een visuele weergave van geluid, waarin je kan zien hoe een geluid verandert over de tijd. Hoe witter, hoe meer energie op die frequentie.")
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
                    feedback = "Dat is correct! Spectrogram C is inderdaad van een mens. {}".format(
                        appendix)
                else:
                    feedback = "Helaas! Je antwoord was onjuist. Het geluid van spectrogram C is van een mens. {}".format(
                        appendix)
            elif rounds_passed == 2:
                if last_result.score == cls.SCORE_CORRECT:
                    feedback = "Dat is correct! Geluid A is inderdaad de Franse baby."
                else:
                    feedback = "Helaas! Geluid A is de de Franse baby."

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback).action()
        return [score]

    @classmethod
    def get_round1(cls, session):
        result_pk = cls.prepare_result(
            session, section=None, expected_response="C")

        # Question
        question = ButtonArrayQuestion(
            question="Welk spectrogram toont het geluid van een mens?",
            key='expected_spectrogram',
            choices={
                'A': 'A',
                'B': 'B',
                'C': 'C',
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])

        image_trial = HTML(
            html='<img src="{}" style="height:calc(100% - 260px);max-height:326px;max-width: 100%;"/>'.format(
                "/images/experiments/toontjehoger/preverbal_1.webp"),
            form=form,
            title=cls.TITLE,
            result_id=result_pk
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
            'spectrograms': ["/images/experiments/toontjehoger/spectrogram-trumpet.webp", "/images/experiments/toontjehoger/spectrogram-whale.webp", "/images/experiments/toontjehoger/spectrogram-human.webp"]
        }
        playback = Playback(
            [sectionA, sectionB, sectionC], player_type=Playback.TYPE_SPECTROGRAM, play_config=play_config)

        # Question
        question = ChoiceQuestion(
            question="",
            key='dummy',
            choices={
                "_": "Volgende",
            },
            view='BUTTON_ARRAY',
            submits=True
        )
        form = Form([question], create_result=False)

        # Trial
        trial_config = {
            'style': 'neutral primary-form',
        }

        trial = Trial(
            config=trial_config,
            playback=playback,
            feedback_form=form,
            title=cls.TITLE,
        ).action()
        return [trial]

    @classmethod
    def get_round2(cls, round, session):
        # Create result
        result_pk = cls.prepare_result(
            session, section=None, expected_response="A")

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
        question = ChoiceQuestion(
            question="Welke baby is in Frankrijk geboren?",
            key='baby',
            choices={
                "A": "A",
                "B": "B",
            },
            view='BUTTON_ARRAY',
            submits=True,
            result_id=result_pk
        )
        form = Form([question])

        # Trial
        trial_config = {
            'style': 'neutral',
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
        score = cls.get_score(session, session.rounds_passed())

        # Final
        final_text = "Goed gedaan! jouw relatief gehoor is uitstekend!" if session.final_score >= 2 * \
            cls.SCORE_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=cls.rank(session),
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
