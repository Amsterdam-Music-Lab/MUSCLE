from django.utils.translation import gettext_lazy as _
from dataclasses import dataclass
from typing import Optional, Dict

from experiment.serializers import serialize_social_media_config, SocialMediaConfigDto
from session.models import Session

from .base_action import BaseAction


@dataclass
class ButtonResponse:
    """
    Button configuration for an optional call-to-action button.

    Attributes:
        text (str): The text displayed on the button.
        link (str): The URL or path to navigate to when the button is clicked.
    """

    text: str
    link: str


@dataclass
class LogoResponse:
    """
    Logo configuration for branding or visual identification on the final screen.

    Attributes:
        image (str): The URL of the logo image to display.
        link (str): The URL to navigate to when the logo is clicked.
    """

    image: str
    link: str


@dataclass
class FinalActionResponse:
    """
    FinalActionResponse represents the structure of the final action data.

    Attributes:
        view (str): A string identifying the view type, usually "FINAL".
        score (float): The participant’s final numeric score at the end of the experiment or session.
        rank (Optional[str]): The participant’s performance rank (e.g., "GOLD", "SILVER") or None if no rank is determined.
        final_text (Optional[str]): A concluding message encouraging sharing, replaying, or reflecting on the results.
        button (Optional[ButtonResponse]): Configuration for an optional call-to-action button.
        points (str): The label for the scoring unit (e.g., "points"), typically localized.
        action_texts (Dict[str, str]): A dictionary of localized strings for various interactive elements.
        title (str): The title displayed prominently on the final screen, typically summarizing the result.
        social (Optional[SocialMediaConfigDto]): Configuration for social media sharing.
        show_profile_link (bool): Whether to display a link to the participant's profile.
        show_participant_link (bool): Whether to show a participant-related link or data.
        feedback_info (Optional[Dict[str, str]]): Additional details enabling a feedback section.
        participant_id_only (bool): If True, only display the participant ID without linking it.
        logo (Optional[LogoResponse]): Optional logo configuration for branding.
    """

    view: str
    score: float
    rank: Optional[str]
    final_text: Optional[str]
    button: Optional[ButtonResponse]
    points: str
    action_texts: Dict[str, str]
    title: str
    social: Optional[SocialMediaConfigDto]
    show_profile_link: bool
    show_participant_link: bool
    feedback_info: Optional[Dict[str, str]]
    participant_id_only: bool
    logo: Optional[LogoResponse]


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
        button (Optional[ButtonResponse]): Optional call-to-action button configuration. For example:
                                            {"text": "Play again", "link": "/{experiment_slug}"}.
        points (Optional[str]): The label for the score units (e.g., "points"). Defaults to a localized "points".
        rank (Optional[str]): The participant's rank (e.g., "GOLD"). If not provided, no rank is displayed.
        show_profile_link (bool): If True, display a link to the participant's profile.
        show_participant_link (bool): If True, display a participant-related link or information.
        show_participant_id_only (bool): If True, only the participant ID is shown, without a link.
        feedback_info (Optional[Dict[str, str]]): Optional dictionary containing feedback-related data. For example:
                                                  {"header": "Feedback", "prompt": "Tell us what you think", "button_text": "Submit"}.
        total_score (Optional[float]): Explicit final score. If None, this is derived from the session.
        logo (Optional[LogoResponse]): Optional logo configuration for branding. For example:
                                        {"image": "/static/logo.png", "link": "https://example.com"}.

    Note:
        The `action()` method returns a `FinalActionResponse` that can be consumed by the frontend
        to render the final screen.
    """

    ID = "FINAL"

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
        button: Optional[ButtonResponse] = None,
        points: Optional[str] = None,
        rank: Optional[str] = None,
        show_profile_link: bool = False,
        show_participant_link: bool = False,
        show_participant_id_only: bool = False,
        feedback_info: Optional[Dict[str, str]] = None,
        total_score: Optional[float] = None,
        logo: Optional[LogoResponse] = None,
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

        if total_score is None:
            self.total_score = self.session.total_score()
        else:
            self.total_score = total_score

        if points is None:
            self.points = _("points")
        else:
            self.points = points

    def action(self) -> FinalActionResponse:
        return FinalActionResponse(
            view=self.ID,
            score=self.total_score,
            rank=self.rank,
            final_text=self.final_text,
            button=self.button,
            points=self.points,
            action_texts={
                "play_again": _("Play again"),
                "profile": _("My profile"),
                "all_experiments": _("All experiments"),
            },
            title=self.title,
            social=self.get_social_media_config(self.session),
            show_profile_link=self.show_profile_link,
            show_participant_link=self.show_participant_link,
            feedback_info=self.feedback_info,
            participant_id_only=self.show_participant_id_only,
            logo=self.logo,
        )

    def get_social_media_config(self, session: Session) -> Optional[SocialMediaConfigDto]:
        """
        Retrieve social media configuration related to the experiment.

        Args:
            session (Session): The current participant's session object.

        Returns:
            Optional[SocialMediaConfigDto]: Social media configuration for sharing results.
            Returns None if no configuration is available.
        """
        experiment = session.block.phase.experiment
        if hasattr(experiment, "social_media_config") and experiment.social_media_config:
            return serialize_social_media_config(experiment.social_media_config, session.total_score())
        return None
