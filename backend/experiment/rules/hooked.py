from django.utils.translation import gettext_lazy as _

from .base import Base

class Hooked(Base):
    """ Inherit from these rules to set up a variant
    of the Hooked on Music game
    """
    
    def calculate_score(self, session, data):
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