from .hooked import Hooked
import random
from django.utils.translation import gettext_lazy as _
from experiment.actions import Trial
from experiment.actions.playback import Playback
from experiment.actions.form import BooleanQuestion, Form
from experiment.actions.styles import STYLE_BOOLEAN_NEGATIVE_FIRST
from experiment.actions.wrappers import song_sync
from result.utils import prepare_result


class Eurovision2020(Hooked):
    """Rules for the Eurovision 2020 version of the Hooked experiment.

    Based on the MBCS internship projects of Ada Orken and and Leanne Kuiper.
    """

    ID = 'EUROVISION_2020'
    play_method = 'BUFFER'

    def plan_sections(self, session):
        """Set the plan of tracks for a session.

        N.B. Assumes exactly one segment each of tags 1, 2, and 3 per song!
        """

        # Which songs are available?
        free_song_set = set(session.playlist.song_ids({'tag__lt': 3}))
        old_new_song_set = set(session.playlist.song_ids({'tag__gt': 0}))

        # How many sections do we need?
        n_old = round(0.17 * session.experiment.rounds)
        n_new = round(0.33 * session.experiment.rounds) - n_old
        n_free = session.experiment.rounds - 2 * n_old - n_new

        # Assign songs.
        old_songs = random.sample(old_new_song_set, k=n_old)
        free_songs = random.sample(free_song_set - set(old_songs), k=n_free)
        new_songs = \
            random.sample(
                free_song_set - set(old_songs + free_songs),
                k=n_new
            )

        # Assign tags for Block 2. Technically 1 and 2 are also OK for the
        # 'free' sections in Block 1, but it is easier just to set tag 0.
        free_tags = [0] * n_free
        old_tags_1 = random.choices([1, 2], k=n_old)
        condition = random.choice(['same', 'different', 'karaoke'])
        if condition == 'karaoke':
            old_tags_2 = [3] * n_old
            new_tags = [3] * n_new
        # Reverse tags 1 and 2 for the 'different' condition.
        elif condition == 'different':
            old_tags_2 = [3 - tag for tag in old_tags_1]
            new_tags = random.choices([1, 2], k=n_new)
        else:  # condition == 'same'
            old_tags_2 = old_tags_1
            new_tags = random.choices([1, 2], k=n_new)

        # Randomise.
        permutation_1 = random.sample(range(n_free + n_old), n_free + n_old)
        permutation_2 = random.sample(range(n_old + n_new), n_old + n_new)
        plan = {
            'n_song_sync': n_free + n_old,
            'n_heard_before': n_old + n_new,
            'condition': condition,
            'songs': (
                [(free_songs + old_songs)[i] for i in permutation_1]
                + [(old_songs + new_songs)[i] for i in permutation_2]
            ),
            'tags': (
                [(free_tags + old_tags_1)[i] for i in permutation_1]
                + [(old_tags_2 + new_tags)[i] for i in permutation_2]
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
            songs = plan['songs']
            tags = plan['tags']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        # Get section.
        section = None
        if round_number <= len(songs) and round_number <= len(tags):
            section = \
                session.playlist.get_section(
                    {'tag': str(tags[round_number])},
                    [songs[round_number]]
                )
        if not section:
            print("Warning: no next_song_sync section found")
            section = session.playlist.get_section()
        return song_sync(session, section, title=self.get_trial_title(session, round_number))

    def next_heard_before_action(self, session):
        """Get next heard_before action for this session."""

        # Load plan.
        try:
            plan = session.load_json_data()['plan']
            songs = plan['songs']
            tags = plan['tags']
            novelty = plan['novelty']
        except KeyError as error:
            print('Missing plan key: %s' % str(error))
            return None

        round_number = self.get_current_round(session)

        # Get section.
        section = None
        if round_number <= len(songs) and round_number <= len(tags):
            section = session.playlist.get_section(
                {'tag': str(tags[round_number])},
                [songs[round_number]]
            )

        if not section:
            print("Warning: no heard_before section found")
            section = session.playlist.get_section()

        playback = Playback(
            sections=[section],
            play_config={'ready_time': 3, 'show_animation': True,
                         'play_method': self.play_method},
            preload_message=_('Get ready!'))
        expected_result = novelty[round_number]
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
