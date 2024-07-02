import random
from django.utils.translation import gettext_lazy as _

from backend.section.models import Playlist, Section, Song
from backend.session.models import Session
from experiment.actions import Trial
from experiment.actions.playback import Autoplay
from experiment.actions.form import BooleanQuestion, Form
from experiment.actions.styles import STYLE_BOOLEAN_NEGATIVE_FIRST
from experiment.actions.wrappers import song_sync
from result.utils import prepare_result
from .hooked import Hooked


class Kuiper2020(Hooked):
    """Rules for the Christmas version of the Hooked experiment.

    Based on the MBCS internship projects of Leanne Kuiper.
    """

    ID = 'KUIPER_2020'

    def get_song_sync_sections(self, session: Session, songs: list[Song], n_song_sync_rounds: int) -> list[int]:
        n_returning_sections = round(n_song_sync_rounds / 4)
        returning_sections = [session.get_random_section(
            {'song__id': song.id, 'tag__gt': 0}).id for song in songs[:n_returning_sections]]
        free_sections = [session.get_random_section(
            {'song__id': song.id}).id for song in songs[n_returning_sections:n_song_sync_rounds]]
        return returning_sections + free_sections

    def get_heard_before_old_sections(self, session: Session, song_sync_sections: list[int], n_heard_before_old_rounds: int) -> list[int]:
        condition = random.sample('same', 'different')
        session.save_json_data({'condition': condition})
        if condition == 'same':
            return song_sync_sections[:n_heard_before_old_rounds]
        else:
            return [session.get_random_section({'song__id': section.song.id}, exclude={
                'tag': section.tag}) for section in song_sync_sections]

    def next_song_sync_action(self, session):
        """Get next song_sync section for this session."""

        # Load plan.
        round_number = self.get_current_round(session)
        try:
            plan = session.load_json_data()['plan']
            sections = plan['sections']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if round_number <= len(sections):
            section = \
                session.playlist.section_set.get(id=sections[round_number])
        if not section:
            print("Warning: no next_song_sync section found")
            section = session.section_from_any_song()
        return song_sync(session, section, title=self.get_trial_title(session, round_number))

    def next_heard_before_action(self, session):
        """Get next heard_before action for this session."""

        # Load plan.
        try:
            plan = session.load_json_data()['plan']
            sections = plan['sections']
            novelty = plan['novelty']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        round_number = self.get_current_round(session)
        # Get section.
        section = None
        if round_number <= len(sections):
            section = \
                session.playlist.section_set.get(id=sections[round_number])
        if not section:
            print("Warning: no heard_before section found")
            section = session.section_from_any_song()

        playback = Autoplay(
            [section],
            show_animation=True,
            preload_message=_('Get ready!')
        )
        expected_result=novelty[round_number]
        # create Result object and save expected result to database
        result_pk = prepare_result('heard_before', session, section=section,
                                   expected_response=expected_result, scoring_rule='REACTION_TIME')
        form = Form([BooleanQuestion(
            key='heard_before',
            choices={
                'new': _("No"),
                'old': _("Yes"),
            },
            question=_("Did you hear this song in previous rounds?"),
            result_id=result_pk,
            style=STYLE_BOOLEAN_NEGATIVE_FIRST,
            submits=True)])
        config = {
            'auto_advance': True,
            'decision_time': self.heard_before_time
        }
        trial = Trial(
            title=self.get_trial_title(session, round_number),
            playback=playback,
            feedback_form=form,
            config=config,
        )
        return trial

    # def validate_playlist(self, playlist: Playlist):
    #     errors = super().validate_playlist(playlist)
    #     return errors
