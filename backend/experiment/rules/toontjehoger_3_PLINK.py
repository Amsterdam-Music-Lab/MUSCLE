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


class ToontjeHoger3PLINK(Base):
    ID = 'TOONTJE_HOGER_3_PLINK'

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

        # If the number of results equals the number of experiment.rounds,
        # close the session and return data for the final_score view.
        if session.rounds_complete():

            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            return combine_actions(
                Score().action(session),
                Final(
                    session=session,
                    final_text=cls.final_score_message(session),
                    rank=cls.rank(session)
                ).action()
            )

        last_result = session.last_result()

        # First round
        if not last_result:
            return combine_actions(cls.get_song_sync_view(session));

        # Other rounds
        return combine_actions(
            cls.get_song_sync_view(session)
        )

    @classmethod
    def get_song_sync_view(cls, session):
        section = session.section_from_unused_song()
        return SongSync.action(
            session=session,
            section=section
        )

    @classmethod
    def get_recognize_view(cls, session):
        section = session.section_from_unused_song()
        section2 = session.section_from_unused_song()
        result_pk = Base.prepare_result(session, section)

        # Get song sections
        all_sections = session.all_sections()
        choices = {}
        for section in all_sections:
            label = section.song_label()
            choices[label] = label

        question = DropdownQuestion(
            question=_('Noem de artiest en de titel van het nummer'),
            key='recognize',
            choices=choices,
            result_id=result_pk,
        )
        form = Form([question])
        play_config = {
            'show_animation': True,
            #'ready_time': 2,
        }
        playback = Playback([section, section2], play_config=play_config,
                            preload_message=_('Get ready!'), player_type=Playback.TYPE_BUTTON)
        playback = Playback([section, section2], play_config=play_config,
                            preload_message=_('Get ready!'), player_type=Playback.TYPE_MULTIPLAYER)
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Toontje Hoger'),
        )
        return view.action()
    

    @classmethod
    def get_button_view(cls, session):
        section = session.section_from_unused_song()
        section2 = session.section_from_unused_song()
        result_pk = Base.prepare_result(session, section)
        print("{}".format(result_pk))
        # Get song sections
        all_sections = session.all_sections()
        choices = {}
        for section in all_sections:
            label = section.song_label()
            choices[label] = label

        question1 = DropdownQuestion(
            question=_('Noem de artiest en de titel van het nummer'),
            key='recognize',
            choices=choices,
            result_id=result_pk,
        )

        question2 = ChoiceQuestion(
            key='dontknow',
            choices={
                'dontknow': _('Ik weet het niet'),
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )

        

        form = Form([question1])
        play_config = {
            'show_animation': True,
            #'ready_time': 2,
        }
        playback = Playback([section, section2], play_config=play_config,
                            preload_message=_('Get ready!'), player_type=Playback.TYPE_BUTTON)
        playback = Playback([section, section2, section, section2], play_config=play_config,
                            preload_message=_('Get ready!'), player_type=Playback.TYPE_MULTIPLAYER)

        # playback = Playback([section], play_config=play_config,
        #                     preload_message=_('Get ready!'), player_type=Playback.TYPE_AUTOPLAY)

        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Toontje Hoger'),
        )
        return view.action()

    @staticmethod
    def calculate_score(result, form_element, data):
        # a result's score is used to keep track of how many correct results were in a row
        # for catch trial, set score to 2 -> not counted for calculating turnpoints
        print("{}".format(result));
        return None