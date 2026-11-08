from typing import Optional, TypedDict

from django.utils.translation import gettext_lazy as _

from experiment.models import Rank
from session.models import Session

from .base_action import BaseAction
from .button import Button


class FinalScore(TypedDict):
    value: float
    label: str


class ScoresView(TypedDict):
    session: FinalScore
    relative: FinalScore
    accumulative: FinalScore


class TrophyView(TypedDict):
    label: str
    description: str
    class_name: str


class FinalViewResponse(TypedDict):
    view: str
    title: str
    trophy: TrophyView
    feedback: str
    visualization: str
    scores: ScoresView


class FinalView(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a "final" view, typically shown at the end of an experiment or session.

    This view displays the participant's final score and, optionally, their rank or performance category.
    It can also present navigation elements, such as a "Play again" button or links to other parts of the site.
    Branding elements like a logo or social sharing options can be included to enhance user engagement.
    A feedback section may also be provided if `feedback_info` is supplied.

    The returned data aligns with `FinalViewResponse`, ensuring type consistency and making the structure
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
            If the passed in button does not specify a link, `session.get_current_experiment_link` will be used to link back to the experiment, if it is replayable.

    Note:
        The `action()` method returns a `FinalViewResponse` that can be consumed by the frontend
        to render the final screen.
    """

    view = "FINAL"

    def __init__(
        self,
        session: Session,
        rank: Rank,
        scores: dict,
        title: str = _("Final score"),
        visualization: Optional[str] = None,
        score_label: str = _("points"),
        button: Optional[Button] = None,
    ):
        self.title = title
        self.visualization = visualization
        self.score_label = score_label
        self.rank = rank
        self.scores = scores
        self.button = self.get_button(button, session)
        self.timeline = self.get_timeline(session)

    def action(self) -> FinalViewResponse:
        response = {
            "view": self.view,
            "title": self.title,
            "rank": self.rank.to_dict(),
            "feedback": self.final_feedback_text,
            "visualization": self.visualization,
            "scores": self.get_scores(),
            "timeline": self.timeline,
            "button": self.button,
        }

        return response

    def get_button(self, button: Button, session: Session) -> Optional[Button]:
        """
        Render a button in the Final action if the link back to the experiment page is valid
        """
        if button and button.link is not None:
            return button
        button_link = session.get_current_experiment_link()
        if button_link:
            if button:
                button.link = button_link
                return button
            return Button(label=_("Next"), link=button_link)

    def get_scores(self):
        return {
            "percentile": {"value": self.scores("percentile"), "label": "%"},
            "total": {
                "value": self.scores.get("total"),
                "label": self.score_label,
            },
            "accumulative": {
                "value": self.scores.get("accumulative"),
                "label": self.score_label,
            },
        }

    def get_timeline(self, session: Session):
        return {
            "playedSessions": session.block.experiment.get_played_sessions_count(
                session.participant
            ),
            "timeline": session.block.experiment.timeline.to_dict(),
        }
