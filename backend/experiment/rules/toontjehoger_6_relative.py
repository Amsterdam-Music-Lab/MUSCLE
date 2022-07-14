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
                Step(
                    _("In dit experiment testen we het relatief gehoor"), number=1),
                Step(
                    _("Er volgen nu 3 vragen"), number=2),
            ],
            button_label=_("Start")

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
        return [Score(session, config=config).action()]

    @classmethod
    def get_round1(cls, session):
        # Explain round
        # -----------------
        explainer = Explainer(
            instruction="Vraag 1",
            steps=[
                Step(
                    _("Luister naar de twee melodieën"), number=1),
                Step(
                    _("Hoor jij of deze hetzelfde zijn?"), number=2),
            ],
            button_label=_("Start")
        ).action(step_numbers=False)

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
            'show_continue_button': True  # False
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
            question=_('Waren deze twee melodieën hetzelfde?'),
            key='equal_melodies',
            choices={
                'YES': _('YES'),
                'NO': _('NO'),
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

        return [explainer, play_trial1, play_trial2, trial]

    @classmethod
    def get_round2(cls, session):
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
        playback = Playback([correct_section], play_config=play_config, preload_message=_(
            'Get ready!'), player_type=Playback.TYPE_AUTOPLAY)

        listen_config = {
            'auto_advance': False
        }

        listen = Trial(
            config=listen_config,
            playback=playback,
            title=cls.TITLE,
        )

        # Step 2
        # --------------------

        # Question
        question = ChoiceQuestion(
            question=_(
                'Welke van deze twee melodieën is hetzelfde als de vorige melodie?'),
            key='same_melodie',
            choices={
                section1.pk: _('Melodie A'),
                section2.pk: _('Melodie B'),
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
        trial_config = {'style': 'boolean blue-players'}

        trial = Trial(
            config=trial_config,
            playback=playback,
            feedback_form=form,
            title=cls.TITLE,
        )
        return [listen.action(), trial.action()]

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
            question=_('Welke van deze melodieën is anders dan de rest?'),
            key='different_melodie',
            choices={
                '0': _('A'),
                '1': _('B'),
                '2': _('C'),
                '3': _('D'),
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
        )
        return [trial.action()]

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
            join('info', 'toontjehoger', 'experiment6.html'))
        info = Info(body=body, heading=_("Relatief gehoor"),
                    continue_button=_("Volgende")).action()

        # Final
        final_text = _("Goed gedaan, jouw relatief gehoor is uitstekend!") if session.final_score >= 2 * \
            cls.SCORE_CORRECT else _("Wellicht nog een poging wagen? Er is ruimte voor verbetering.")
        final = Final(
            session=session,
            final_text=final_text,
            rank=cls.rank(session),
            button={'link': 'https://www.amsterdammusiclab.nl',
                    'text': 'Terug naar ToontjeHoger'}
        ).action()

        return [*score, info, final]
