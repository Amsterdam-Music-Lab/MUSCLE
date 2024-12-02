import random

from django.utils.translation import gettext as _

from result.models import Result
from session.models import Session
from .base_action import BaseAction


class Score(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for an intermediate score view

    Relates to client component: Score.js
    """

    ID = 'SCORE'

    def __init__(
        self,
        session: Session,
        title: str = '',
        result: Result = None,
        score: float = None,
        score_message: str = '',
        config: dict = {},
        icon: str = None,
        timer: int = None,
        feedback: str = None,
    ):
        """Score presents feedback to a participant after a Trial
        - session: a Session object
        - title: the title of the score page
        - result: the result for which section or score should be reported
        - score: the score to report, will override result.score
        - score_message: a function which constructs feedback text based on the score
        - config: a dict with the following settings:
            - show_section: whether metadata of the previous section should be shown
            - show_total_score: whether the total score should be shown
        - icon: the name of a themify-icon shown with the view or None
        - timer: int or None. If int, wait for as many seconds until showing the next view
        - feedback: An additional feedback text
        """
        self.session = session
        self.title = title or _('Round {get_rounds_passed} / {total_rounds}').format(
            get_rounds_passed=session.get_rounds_passed(),
            total_rounds=self.session.block.rounds
        )
        self.score = (
            score if score else result.score if result else session.last_score()
        )
        self.score_message = score_message or self.default_score_message
        self.feedback = feedback
        self.config = {
            'show_section': False,
            'show_total_score': False
        }
        if config:
            self.config.update(config)
        self.icon = icon
        self.texts = {
            'score': _('Total Score'),
            'next': _('Next'),
            'listen_explainer': _('You listened to:')
        }
        self.last_song = result.section.song_label() if result else session.last_song()
        self.timer = timer

    def action(self):
        """Serialize score data"""
        # Create action
        action = {
            'view': self.ID,
            'title': self.title,
            'score': self.score,
            'score_message': self.score_message(self.score),
            'texts': self.texts,
            'feedback': self.feedback,
            'icon': self.icon,
            'timer': self.timer
        }
        if self.config['show_section']:
            action['last_song'] = self.last_song
        if self.config['show_total_score']:
            action['total_score'] = self.session.total_score()
        return action

    def default_score_message(self, score):
        """Fallback to generate a message for the given score"""

        # None
        if score is None:
            score = 0
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
