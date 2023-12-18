import random
from django.utils.translation import gettext_lazy as _

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

    def plan_sections(self, session):
        """Set the plan of tracks for a session.

           Assumes that all tags of 1 have a corresponding tag of 2
           with the same group_id, and vice-versa.
        """

        # Which songs are available?
        free_song_set = set(session.playlist.song_ids())
        old_new_song_set = set(session.playlist.song_ids({'tag__gt': 0}))

        # How many sections do we need?
        n_old = round(0.17 * session.experiment.rounds)
        n_new = round(0.33 * session.experiment.rounds) - n_old
        n_free = session.experiment.rounds - 2 * n_old - n_new

        # Assign songs.
        old_songs = random.sample(old_new_song_set, k=n_old)
        free_songs = random.sample(free_song_set - set(old_songs), k=n_free)
        new_songs = \
            random.sample(free_song_set - set(old_songs + free_songs), k=n_new)

        # Assign sections.
        condition = random.choice(['same', 'different'])
        old_sections_1 = [session.section_from_song(s) for s in old_songs]
        if condition == 'same':
            old_sections_2 = old_sections_1
        else:
            old_sections_2 = \
                [session.
                 section_from_any_song(
                     {'group': s.group, 'tag': 3 - int(s.tag)}
                 )
                 for s in old_sections_1]
        free_sections = [session.section_from_song(s) for s in free_songs]
        new_sections = [session.section_from_song(s) for s in new_songs]

        # Get IDs.
        old_ids_1 = [s.id for s in old_sections_1]
        old_ids_2 = [s.id for s in old_sections_2]
        free_ids = [s.id for s in free_sections]
        new_ids = [s.id for s in new_sections]

        # Randomise.
        permutation_1 = random.sample(range(n_free + n_old), n_free + n_old)
        permutation_2 = random.sample(range(n_old + n_new), n_old + n_new)
        plan = {
            'n_song_sync': n_free + n_old,
            'n_heard_before': n_old + n_new,
            'condition': condition,
            'sections': (
                [(free_ids + old_ids_1)[i] for i in permutation_1]
                + [(old_ids_2 + new_ids)[i] for i in permutation_2]
            ),
            'novelty': (
                [(['free'] * n_free + ['old'] * n_old)[i]
                 for i in permutation_1]
                + [(['old'] * n_old + ['new'] * n_new)[i]
                   for i in permutation_2]
            )
        }

        # Save, overwriting existing plan if one exists.
        session.save_json_data({'plan': plan})
        # session.save() is required for persistence
        session.save()

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
            ready_time=3,
            preload_message=_('Get ready!')
        )
        expected_result=novelty[round_number]
        # create Result object and save expected result to database
        result_pk = prepare_result('heard_before', session, section=section, expected_response=expected_result, scoring_rule='REACTION_TIME')
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
            'decision_time': self.timeout
        }
        trial = Trial(
            title=self.get_trial_title(session, round_number),
            playback=playback,
            feedback_form=form,
            config=config,
        )
        return trial

