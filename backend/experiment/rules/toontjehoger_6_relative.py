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
    TITLE = "Toontje Hoger"
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Uitleg",
            steps=[
                Step("In deze minigame kan je testen hoe goed jouw relatieve gehoor is! Relatief gehoor is het vermogen om verschil of gelijkenis tussen tonen te kunnen herkennen."),
                Step("Je krijgt zo eerst twee melodieën te horen.", number=1),
                Step("Geef aan of deze melodieën hetzelfde zijn!", number=2),
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
            return combine_actions(*cls.get_score(session), *cls.get_round2(session))

        # Round 3
        if rounds_passed == 2:
            return combine_actions(*cls.get_score(session), *cls.get_round3(session))

        # Final
        return combine_actions(*cls.get_final_round(session))

    @classmethod
    def get_score(cls, session):
        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config).action()
        return [score]

    @classmethod
    def get_round1(cls, session):
        # Config
        # -----------------
        same_melodies = randint(0, 1) == 1
        section1 = session.section_from_unused_song(
            filter_by={'group': '1', 'tag': 'original'})

        if section1 == None:
            raise Exception("Error: could not find section1 for round 1")
        # Section 2, is equal to section 1 if melodies are the same
        # Else get a section with the same group, but with different tags
        # e.g.
        # section1: artist=a, name=b, tag=original, group=1
        # section2: artist=a, name=b, tag=variation, group=1
        section2 = section1 if same_melodies else session.section_from_any_song(
            filter_by={'artist': section1.artist, 'name': section1.name, 'tag': 'variation'})
        if section2 == None:
            raise Exception("Error: could not find section2 for round 1")

        expected_response = 'YES' if same_melodies else 'NO'
        result_pk = cls.prepare_result(
            session, section=section1, expected_response=expected_response)

        # Play section 1
        # -----------------
        # Player 1
        play_config = {
            'label_style': '',
        }
        playback1 = Playback(
            [section1], player_type=Playback.TYPE_AUTOPLAY, play_config=play_config)

        # Trial 1
        trial_config = {
            'auto_advance': True,
            'show_continue_button': False
        }

        play_trial1 = Trial(
            config=trial_config,
            playback=playback1,
            title=cls.TITLE,
        ).action()

        # Play section 2
        # -----------------
        # Player 2
        play_config = {
            'label_style': '',
        }
        playback2 = Playback(
            [section2], player_type=Playback.TYPE_AUTOPLAY, play_config=play_config)

        play_trial2 = Trial(
            config=trial_config,
            playback=playback2,
            title=cls.TITLE,
        ).action()

        # Ask question
        # -----------------

        # Question
        question = ChoiceQuestion(
            question="Waren deze twee melodieën hetzelfde?",
            key='equal_melodies',
            choices={
                'YES': 'Ja',
                'NO': 'Nee',
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])

        # Trial
        trial = Trial(
            playback=None,
            feedback_form=form,
            title=cls.TITLE,
        ).action()

        return [play_trial1, play_trial2, trial]

    @classmethod
    def get_round2(cls, session):
        # Explainer
        # -----------------
        explainer = Explainer(
            instruction="Vraag 2",
            steps=[
                Step("Je krijgt eenmalig een melodie te horen."),
                Step("Luister goed, want er volgt weer een vraag!"),
            ],
            button_label="Start"
        ).action(step_numbers=True)

        # Config
        # -----------------
        section1 = session.section_from_unused_song(
            filter_by={'group': '2', 'tag': 'original'})
        if section1 == None:
            raise Exception("Error: could not find section1 for round 2")
        section2 = session.section_from_unused_song(
            filter_by={'artist': section1.artist, 'name': section1.name, 'tag': 'variation'})
        if section2 == None:
            raise Exception("Error: could not find section2 for round 2")

        correct_section = section1 if randint(0, 1) == 1 else section2
        expected_response = correct_section.pk
        result_pk = cls.prepare_result(
            session, section=correct_section, expected_response=expected_response)

        # Step 1
        # --------------------

        # Listen
        play_config = {
        }
        playback = Playback(
            [correct_section], play_config=play_config, player_type=Playback.TYPE_AUTOPLAY)

        listen_config = {
            'auto_advance': True,
            'show_continue_button': False
        }

        listen = Trial(
            config=listen_config,
            playback=playback,
            title=cls.TITLE,
        ).action()

        # Step 2
        # --------------------

        # Question
        question = ChoiceQuestion(
            question="Welke van deze twee melodieën is hetzelfde als de vorige melodie?",
            key='same_melodie',
            choices={
                section1.pk: 'Melodie A',
                section2.pk: 'Melodie B',
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])

        # Player
        play_config = {
            'label_style': 'ALPHABETIC',
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
        return [explainer, listen, trial]

    @classmethod
    def get_round3(cls, session):
        # Configuration
        # --------------------
        different_melody = randint(0, 3)

        section_default = session.section_from_unused_song(
            filter_by={'group': '3', 'tag': 'original'})
        if section_default == None:
            raise Exception(
                "Error: could not find section_default for round 3")

        section_different = session.section_from_unused_song(
            filter_by={'artist': section_default.artist, 'name': section_default.name, 'tag': 'variation'})
        if section_different == None:
            raise Exception(
                "Error: could not find section_different for round 3")

        sections = [section_default, section_default,
                    section_default, section_default]
        sections[different_melody] = section_different

        result_pk = cls.prepare_result(
            session, section_default, expected_response=different_melody)

        # Question
        question = ChoiceQuestion(
            question="Welke van deze melodieën is anders dan de rest?",
            key='different_melodie',
            choices={
                '0': 'A',
                '1': 'B',
                '2': 'C',
                '3': 'D',
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])

        # Player
        play_config = {
            'label_style': 'ALPHABETIC',
        }
        playback = Playback(
            sections, player_type=Playback.TYPE_MULTIPLAYER, play_config=play_config)

        # Trial
        trial_config = {'style': 'neutral'}

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
            cls.SCORE_CORRECT else "Wellicht nog een poging wagen? Er is ruimte voor verbetering."
        final = Final(
            session=session,
            final_text=final_text,
            rank=cls.rank(session),
            button={'text': 'Volgende'}
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
