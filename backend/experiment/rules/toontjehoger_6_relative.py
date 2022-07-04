import logging
from django.utils.translation import gettext_lazy as _

from experiment.models import Section
from .views import Trial, Explainer, Step, Score, Final, StartSession, Playlist, SongSync
from .views.form import ChoiceQuestion, Form, DropdownQuestion
from .views.playback import Playback
from .util.actions import render_feedback_trivia
from .base import Base
from .util.actions import combine_actions

logger = logging.getLogger(__name__)

class ToontjeHoger6Relative(Base):
    ID = 'TOONTJE_HOGER_6_RELATIVE'

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Uitleg",
            steps=[
                Step(
                    _("Luister naar een aantal muziekfragmenten."), number=1),
                Step(
                    _("Hoor jij welke melodieën hetzelfde zijn?"), number=2),
                Step(_("Heel veel succes met dit experiment!")),
            ],
            button_label=_("Start")

        ).action(step_numbers=False)

        # 3. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session.
        start_session = StartSession.action()

        return combine_actions(
            explainer,
            playlist,
            start_session
        )

    @classmethod
    def next_round(cls, session, request_session=None):
        """Get action data for the next round"""

        rounds_passed = session.rounds_passed();
        print(rounds_passed)
        # End of the game
        if rounds_passed == 3:

            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            return combine_actions(
                Final(
                    session=session,
                    final_text=cls.final_score_message(session),
                    rank=cls.rank(session)
                ).action()
            )

        # Round 1
        if rounds_passed == 0:
            return cls.get_round1(session)

        # Round 2
        if rounds_passed == 1:
            return cls.get_round2(session)

        # Round 3
        if rounds_passed == 2:
            return cls.get_round3(session)

        # Should not happen
        return None

    @classmethod
    def get_round1(cls, session):
        # TODO: Get section from tag
        section = session.section_from_unused_song()
        section2 = session.section_from_unused_song()

        result_pk = Base.prepare_result(session, section)

        # Question
        question = ChoiceQuestion(
            question=_('Zijn deze twee melodieën hetzelfde?'),
            key='dontknow',
            choices={
                'YES': _('YES'),
                'NO': _('NO'),
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])

        # Player
        play_config = {
            'label_style': '',
        }
        playback = Playback([section, section2], player_type=Playback.TYPE_MULTIPLAYER, play_config=play_config)

        # Trial
        trial_config = {'style': 'boolean blue-players'}

        trial = Trial(
            config=trial_config,
            playback=playback,
            feedback_form=form,
            title=_('Toontje Hoger'),
        )
        return combine_actions(trial.action())
    
    @classmethod
    def get_round2(cls, session):
        # TODO: Get section from tag
        section = session.section_from_unused_song()
        section2 = session.section_from_unused_song()

        result_pk = Base.prepare_result(session, section)

        # Step 1
        # --------------------

        # Listen
        play_config = {
        }
        playback = Playback([section], play_config=play_config, preload_message=_('Get ready!'), player_type=Playback.TYPE_AUTOPLAY);

        listen_config = {
            'auto_advance': True
        }
        
        listen = Trial(
            config=listen_config,
            playback=playback,
            title=_('Toontje Hoger'),
        )

        # Step 2
        # --------------------

        # Question
        question = ChoiceQuestion(
            question=_('Welke van deze twee melodieën is hetzelfde als de vorige melodie?'),
            key='dontknow',
            choices={
                'A': _('Melodie A'),
                'B': _('Melodie B'),
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
        playback = Playback([section, section2], player_type=Playback.TYPE_MULTIPLAYER, play_config=play_config)

        # Trial
        trial_config = {'style': 'boolean blue-players'}

        trial = Trial(
            config=trial_config,
            playback=playback,
            feedback_form=form,
            title=_('Toontje Hoger'),
        )
        return combine_actions(listen.action(), trial.action())

    @classmethod
    def get_round3(cls, session):
        # TODO: Get section from tag
        section = session.section_from_unused_song()
        section2 = session.section_from_unused_song()
        section3 = session.section_from_unused_song()
        section4 = session.section_from_unused_song()

        result_pk = Base.prepare_result(session, section)


        
        # Question
        question = ChoiceQuestion(
            question=_('Welke van deze melodieën is anders dan de rest?'),
            key='dontknow',
            choices={
                'A': _('A'),
                'B': _('B'),
                'C': _('C'),
                'D': _('D'),
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
        playback = Playback([section, section2, section3, section4], player_type=Playback.TYPE_MULTIPLAYER, play_config=play_config)

        # Trial
        trial_config = {'style': 'neutral'}

        trial = Trial(
            config=trial_config,
            playback=playback,
            feedback_form=form,
            title=_('Toontje Hoger'),
        )
        return combine_actions(trial.action())

    @staticmethod
    def calculate_score(result, form_element, data):
        # a result's score is used to keep track of how many correct results were in a row
        # for catch trial, set score to 2 -> not counted for calculating turnpoints
        print("{}".format(result));
        return None