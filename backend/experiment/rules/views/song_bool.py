import math
import random

from django.utils.translation import gettext_lazy as _


class SongBool:  # pylint: disable=too-few-public-methods
    """
    Provide data for a SongBool view that plays a section, shows a question and has yes/no buttons

    Relates to client component: SongBool.js
    """

    ID = 'SONG_BOOL'

    @staticmethod
    def calculate_score(session, data):
        """Calculate score for given result data"""
        score = 0

        # Calculate from the data object
        # If requested keys don't exist, return None
        try:

            config = data['config']
            result = data['result']
            time = result['decision_time']

            # Calculate scores based on result type
            if result['type'] == 'time_passed':
                score = math.ceil(-time)

            else:
                if result['given_result'] == config['expected_result']:
                    # correct
                    score = math.ceil(
                        config['decision_time'] - result['decision_time']
                    )
                else:
                    # wrong
                    score = math.floor(-time)

        except KeyError as error:
            print('KeyError: %s' % str(error))
            return None

        return score

    @staticmethod
    def action(session, instruction, section, expected_result):
        """Get data for song_bool action"""

        # Create action
        action = {
            'view': SongBool.ID,
            'title': _('Round {} / {}').format(session.get_next_round(), session.experiment.rounds),
            'instruction': instruction,
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

        # Config
        action['config'] = {
            'ready_time': 3,
            'decision_time': 15,
            'expected_result': expected_result,
        }

        return action
