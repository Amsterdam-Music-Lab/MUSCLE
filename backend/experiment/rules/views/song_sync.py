import math
import random

from django.utils.translation import gettext_lazy as _

class SongSync:  # pylint: disable=too-few-public-methods
    """
    Provide data for a SongSync view that handles views for song recognition,
    a silence and in- or out-sync continuation of audio playback

    Relates to client component: SongSync.js
    """

    ID = 'SONG_SYNC'

    @staticmethod
    def calculate_score(session, data):
        """Calculate score for given result data"""
        score = 0

        # Calculate from the data object
        # If requested keys don't exist, return None
        try:

            config = data['config']
            result = data['result']

            # Calculate scores based on result type
            if result['type'] == 'time_passed':
                score = math.ceil(-result['recognition_time'])

            elif result['type'] == 'not_recognized':
                score = 0

            elif result['type'] == 'recognized':
                # Get score
                score = math.ceil(
                    config['recognition_time'] - result['recognition_time']
                )

                if config['continuation_correctness'] != result['continuation_correctness']:
                    score *= -1

        except KeyError as error:
            print('KeyError: %s' % str(error))
            return None

        return score

    @staticmethod
    def action(session, section, config={}):
        """Get data for song_sync action, with given section and config"""

        # Create action
        action = {
            'view': SongSync.ID,
            'title': _('Round {} / {}').format(session.get_next_round(), session.experiment.rounds),
            'instructions': {
                'recognize': _('Do you recognise this song?'),
                'imagine': _('Keep imagining the music'),
                'correct': _('Did the track come back in the right place?'),
                'ready': _('Get ready!')
            },
            'buttons': {
                'yes': _('Yes'),
                'no': _('No')
            } 
        }

        # Section
        action['section'] = {
            'id': section.id,
            'artist': section.artist,
            'song': section.name,
            'url': section.absolute_url(),
        }

        # Default random continuation correctness
        continuation_correctness = random.randint(0, 1) == 1

        # Config
        default_config = {
            'ready_time': 3,
            'recognition_time': 15,
            'silence_time': 4,
            'sync_time': 15,
            'continuation_offset': random.randint(100, 150) / 10 if not continuation_correctness else 0,
            'continuation_correctness': continuation_correctness,
        }

        action['config'] = {
            **default_config,
            **config,
        }

        return action
