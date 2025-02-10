import random
from typing import Optional, TypedDict

from django.utils.translation import gettext as _

from result.models import Result
from session.models import Session
from .base_action import BaseAction


class ScoreConfig(TypedDict):
    """
    Configuration for the Score action

    Args:
        show_section: whether metadata of the previous section should be shown, often the title of the last played song
        show_total_score: whether the total score should be shown in the view
    """

    show_section: bool
    show_total_score: bool


class Score(BaseAction):
    """
    Provide data for a score view, presenting feedback to a participant after a Trial.

    Args:
        session (Session): a Session object
        title (str): the title of the score page
        result (Optional[Result]): the result for which section and/or score should be reported
        score (Optional[float]): the score to report, will override result.score
        score_message: a function which constructs feedback text based on the score
        config (Optional[ScoreConfig]): a dict with the following settings:
        icon (Optional[str]): the name of a themify-icon shown with the view or None
        timer (Optional[int]): int or None. If int, wait for as many seconds until showing the next view
        feedback (Optional[str]): An additional feedback text

    Note:
        Relates to the Score.tsx component in the frontend
    """

    view = "SCORE"

    def __init__(
        self,
        session: Session,
        title: str = "",
        result: Optional[Result] = None,
        score: Optional[float] = None,
        score_message: str = "",
        config: Optional[ScoreConfig] = None,
        icon: Optional[str] = None,
        timer: Optional[int] = None,
        feedback: Optional[str] = None,
    ):
        self.title = title or _("Round {get_rounds_passed} / {total_rounds}").format(
            get_rounds_passed=session.get_rounds_passed(),
            total_rounds=session.block.rounds,
        )
        self.session = session
        self.score = self.get_score(score, result)
        self.score_message = score_message or self.default_score_message(self.score)
        self.feedback = feedback
        self.config = {"show_section": False, "show_total_score": False}
        if config:
            self.config.update(config)
        self.icon = icon
        self.texts = {"score": _("Total Score"), "next": _("Next"), "listen_explainer": _("You listened to:")}
        self.last_song = result.section.song_label() if result else session.last_song()
        self.timer = timer

    def action(self) -> dict:
        """Serialize score data

        Returns:
            dictionary with the relevant data for the Score.tsx view
        """
        # Create action
        action = {
            "view": self.view,
            "title": self.title,
            "score": self.score,
            "score_message": self.score_message,
            "texts": self.texts,
            "feedback": self.feedback,
            "icon": self.icon,
            "timer": self.timer,
        }
        if self.config["show_section"]:
            action["last_song"] = self.last_song
        if self.config["show_total_score"]:
            action["total_score"] = self.session.total_score()
        return action

    def get_score(self, score: Optional[float] = None, result: Optional[Result] = None) -> float:
        """Retrieve the last relevant score, fall back to session.last_score() if neither score nor result are defined

        Args:
            score: the score passed from the rules file (optional)
            result: a Result object passed from the rules file (opional)
        """
        if score:
            return score
        elif result:
            return result.score
        else:
            return self.session.last_score()

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
