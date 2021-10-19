import random

from django.utils.translation import gettext as _

class Score:  # pylint: disable=too-few-public-methods
    """
    Provide data for an intermediate score view

    Relates to client component: Score.js 
    """

    ID = 'SCORE'

    @staticmethod
    def action(session, include_section=True):
        """Get data for score action"""

        # Create action
        score = session.last_score()
        action = {
            'view': Score.ID,
            'title': _('Round {} / {}').format(session.rounds_passed(), session.experiment.rounds),
            'last_song': session.last_song() if include_section else None,
            'score': score,
            'score_message': Score.score_message(score),
            'total_score': session.total_score(),
            'texts': {
                'score': _('Score'),
                'next': _('Next'),
                'listen_explainer': _('You listened to:')
            }
        }
        return action

    @staticmethod
    def score_message(score):
        """Generate a message for the given score"""
        # Zero
        if score == 0:
            # "Too bad!", "Come on!", "Try another!", "Try again!"
            return random.choice([_("No points")])
        # Negative
        if score < 0:
            return random.choice([_("Incorrect")])  # "Too bad!", "Fail!", "Nooo!"
        # Positive
        # "Well done!", "Nice job!", "Great one!", "Score!", "You're good!", "Awesome!", "Nice one!"
        return random.choice([_("Correct")])
