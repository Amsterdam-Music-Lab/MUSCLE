import re
from typing import Optional, Dict, TypedDict

from django.utils.translation import gettext_lazy as _

from experiment.actions.types import FeedbackInfo
from experiment.serializers import serialize_social_media_config, SocialMediaConfigConfiguration
from session.models import Session

from .base_action import BaseAction


class ButtonConfiguration(TypedDict):
    """
    Button configuration for an optional call-to-action button.

    Attributes:
        text (str): The text displayed on the button.
        link (str): The URL or path to navigate to when the button is clicked.
    """

    text: str
    link: str


class LogoConfiguration(TypedDict):
    """
    Logo configuration for branding or visual identification on the final screen.

    Attributes:
        image (str): The URL of the logo image to display.
        link (str): The URL to navigate to when the logo is clicked.
    """

    image: str
    link: str


class FinalActionResponse(TypedDict):
    view: str
    score: float
    percentile: Optional[float]
    rank: Optional[str]
    final_text: Optional[str]
    button: Optional[ButtonConfiguration]
    points: str
    action_texts: Dict[str, str]
    title: str
    social: Optional[SocialMediaConfigConfiguration]
    show_profile_link: bool
    show_participant_link: bool
    feedback_info: Optional[Dict[str, str]]
    participant_id_only: bool
    logo: Optional[LogoConfiguration]


class Final(BaseAction):  # pylint: disable=too-few-public-methods
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
        final_text (Optional[str]): An optional concluding message (e.g., "Thanks for participating!").
        button (Optional[ButtonConfiguration]): Optional call-to-action button configuration. For example:
                                            {"text": "Play again", "link": "/{experiment_slug}"}.
        points (Optional[str]): The label for the score units (e.g., "points"). Defaults to a localized "points".
        rank (Optional[str]): The participant's rank (e.g., "GOLD"). If not provided, no rank is displayed.
        show_profile_link (bool): If True, display a link to the participant's profile.
        show_participant_link (bool): If True, display a participant-related link or information.
        show_participant_id_only (bool): If True, only the participant ID is shown, without a link.
        feedback_info (Optional[Dict[str, str]]): Optional dictionary containing feedback-related data. For example:
                                                  {"header": "Feedback", "prompt": "Tell us what you think", "button_text": "Submit"}.
        total_score (Optional[float]): Explicit final score. If None, this is derived from the session.
        logo (Optional[LogoConfiguration]): Optional logo configuration for branding. For example:
                                        {"image": "/static/logo.png", "link": "https://example.com"}.

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
        final_text: Optional[str] = None,
        button: Optional[ButtonConfiguration] = None,
        points: Optional[str] = None,
        rank: Optional[str] = None,
        show_profile_link: bool = False,
        show_participant_link: bool = False,
        show_participant_id_only: bool = False,
        feedback_info: FeedbackInfo | None = None,
        total_score: Optional[float] = None,
        logo: Optional[LogoConfiguration] = None,
        percentile: Optional[float] = None,  # new argument
    ):
        self.session = session
        self.title = title
        self.final_text = final_text
        self.button = button
        self.rank = rank
        self.show_profile_link = show_profile_link
        self.show_participant_link = show_participant_link
        self.show_participant_id_only = show_participant_id_only
        self.feedback_info = feedback_info
        self.logo = logo
        self.percentile = percentile

        if total_score is None:
            self.total_score = self.session.total_score()
        else:
            self.total_score = total_score

        if points is None:
            self.points = _("points")
        else:
            self.points = points

    def action(self) -> FinalActionResponse:
        response: FinalActionResponse = {
            "view": self.view,
            "score": self.total_score,
            "percentile": self.percentile,
            "rank": self.rank,
            "final_text": self.wrap_plain_final_text(),
            "button": self.button,
            "points": self.points,
            "action_texts": {
                "play_again": _("Play again"),
                "profile": _("My profile"),
                "all_experiments": _("All experiments"),
            },
            "title": self.title,
            "social": self.get_social_media_config(self.session),
            "show_profile_link": self.show_profile_link,
            "show_participant_link": self.show_participant_link,
            "feedback_info": self.feedback_info,
            "participant_id_only": self.show_participant_id_only,
            "logo": self.logo,
        }

        return response

    def get_social_media_config(self, session: Session) -> Optional[SocialMediaConfigConfiguration]:
        experiment = session.block.phase.experiment
        if hasattr(experiment, "social_media_config") and experiment.social_media_config:
            return serialize_social_media_config(experiment.social_media_config, session.total_score())
        return None

    def wrap_plain_final_text(self):
        '''check if `final_text` starts with a html tag
        If not, wrap it in a `<center>` element for better alignment
        '''
        tag_pattern = re.compile('<[a-z]*>')
        if self.final_text and not re.match(tag_pattern, str(self.final_text)):
            return f'<center>{self.final_text}</center>'
        return self.final_text
