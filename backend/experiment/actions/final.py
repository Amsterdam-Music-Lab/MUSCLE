from typing import Optional, TypedDict

from django.utils.translation import gettext_lazy as _

from experiment.actions.utils import get_experiment_url
from experiment.models import Progress, Rank
from session.models import Session

from .base_action import BaseAction
from .button import Button


class FinalScore(TypedDict):
    value: float
    label: str


class ScoresAction(TypedDict):
    session: FinalScore
    relative: FinalScore
    accumulative: FinalScore


class AchievementAction(TypedDict):
    label: str
    description: str
    class_name: str


class RewardAction(TypedDict):
    every_n: int
    image: str


class ProgressAction(TypedDict):
    total_sessions: int
    rewards: Optional[list[RewardAction]]


class FinalActionResponse(TypedDict):
    view: str
    title: str
    achievement: AchievementAction
    feedback: str
    visualization: str
    scores: ScoresAction
    progress: ProgressAction


class FinalAction(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a "final" view, typically shown at the end of an experiment or session.

    This view displays the participant's final score and, optionally, their rank or performance category.
    It can also present navigation elements, such as a "Play again" button or links to other parts of the site.
    Branding elements like a logo or social sharing options can be included to enhance user engagement.
    A feedback section may also be provided if `feedback_info` is supplied.

    The returned data aligns with `FinalActionResponse`, ensuring type consistency and making the structure
    clear for both developers and documentation readers. It can be consumed by a frontend component
    (e.g.,
    [Final.tsx](https://amsterdam-music-lab.github.io/MUSCLE/storybook/?path=/story/final--default)) to render the final screen.

    Args:
        session (Session): The current session object associated with the participant.
        title (str): The title displayed at the top of the final view. Defaults to a localized "Final score".
        visualization(str): The visualization displayed to show the participant's relative score
        score_label (str): Text to display with score. Default: _("points)
        button (Optional[Button]): Optional button configuration. For example:
            {"label": "Play again", "link": "/{experiment_identifier}"}. If not provided, a default button with label "Next" will be rendered, unless the experiment is not replayable.
            If the passed in button does not specify a link, `get_experiment_url` will be used to link back to the experiment, if it is replayable.

    Note:
        The `action()` method returns a `FinalActionResponse` that can be consumed by the frontend
        to render the final screen.
    """

    view = "FINAL"

    RANKS = {
        "PLASTIC": {"text": _("plastic"), "class": "plastic"},
        "BRONZE": {"text": _("bronze"), "class": "bronze"},
        "SILVER": {"text": _("silver"), "class": "silver"},
        "GOLD": {"text": _("gold"), "class": "gold"},
        "PLATINUM": {"text": _("platinum"), "class": "platinum"},
        "DIAMOND": {"text": _("diamond"), "class": "diamond"},
    }

    def __init__(
        self,
        session: Session,
        title: str = _("Final score"),
        visualization: Optional[str] = None,
        score_label: str = _("points"),
        button: Optional[Button] = None,
    ):
        self.title = title
        self.visualization = visualization
        self.score_label = score_label
        self.button = self.get_button(button, session)

    def action(self) -> FinalActionResponse:
        response: FinalActionResponse = {
            "view": self.view,
            "title": self.title,
            "achievement": self.rank.get_achievement_data(),
            "feedback": self.rank.get_feedback_data(self.relative_score),
            "visualization": self.visualization,
            "scores": {
                "relative": {"value": self.relative_score, "label": "%"},
                "session": {
                    "value": self.score,
                    "label": self.score_label,
                },
                "total": {
                    "value": self.accumulative_score,
                    "label": self.score_label,
                },
            },
            "progress": self.progress.convert_to_action(),
            "button": self.button,
        }

        return response

    def set_scores(
        self,
        score: float = None,
        relative_score: float = 100,
        accumulative_score: float = None,
    ):
        self.score = score
        self.relative_score = relative_score
        self.accumulative_score = accumulative_score

    def set_progress(self, progress: Progress):
        self.progress = progress

    def set_active_rank(self, rank: Rank):
        self.rank = rank

    def get_button(self, button: Button, session: Session) -> Optional[Button]:
        """
        Render a button in the Final action if the link back to the experiment page is valid
        """
        if button and button.link is not None:
            return button
        button_link = get_experiment_url(session)
        if button_link:
            if button:
                button.link = button_link
                return button
            return Button(label=_("Next"), link=button_link)
