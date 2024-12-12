from django.utils.translation import gettext_lazy as _
from typing import TypedDict

from experiment.serializers import serialize_social_media_config, SocialMediaConfigDto
from session.models import Session

from .base_action import BaseAction


class ButtonDto(TypedDict):
    """
    Button configuration for an optional call-to-action button.

    Attributes:
        text (str): The text displayed on the button.
        link (str): The URL or path to navigate to when the button is clicked.
    """

    text: str
    link: str


class LogoDto(TypedDict):
    """
    Logo configuration for branding or visual identification on the final screen.

    Attributes:
        image (str): The URL of the logo image to display.
        link (str): The URL to navigate to when the logo is clicked.
    """

    image: str
    link: str


class FinalActionDto(TypedDict):
    """
    FinalActionDto represents the structure of the final action data transfer object.

    Attributes:
        view (str): A string identifying the view type, usually "FINAL".
        score (float): The participant’s final numeric score at the end of the experiment or session.
        rank (str | None): The participant’s performance rank (e.g., "GOLD", "SILVER") or None if no rank is determined.
        final_text (str | None): A concluding message encouraging sharing, replaying, or reflecting on the results.
        button (ButtonDto | None): Configuration for an optional call-to-action button.
                                   For example: {"text": "Play again", "link": "/{experiment_slug}"}.
        points (str): The label for the scoring unit (e.g., "points"), typically localized.
        action_texts (dict): A dictionary of localized strings for various interactive elements. Typically includes:
                             - "play_again": _("Play again")
                             - "profile": _("My profile")
                             - "all_experiments": _("All experiments")
        title (str): The title displayed prominently on the final screen, typically summarizing the result (e.g., "Final score").
        social (SocialMediaConfigDto | None): Configuration for social media sharing. If present, it specifies channels,
                                              content, and links for participants to share their results.
        show_profile_link (bool): Whether to display a link to the participant's profile.
        show_participant_link (bool): Whether to show a participant-related link or data.
        feedback_info (dict | None): Additional details enabling a feedback section where participants can leave remarks or questions.
        participant_id_only (bool): If True, only display the participant ID without linking it, for a more anonymized final screen.
        logo (LogoDto | None): Optional logo configuration for branding. For example:
                               {"image": "/static/logo.png", "link": "https://example.com"}.
    """

    view: str
    score: float
    rank: str | None
    final_text: str | None
    button: ButtonDto | None
    points: str
    action_texts: dict
    title: str
    social: SocialMediaConfigDto | None
    show_profile_link: bool
    show_participant_link: bool
    feedback_info: dict | None
    participant_id_only: bool
    logo: LogoDto | None


class Final(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a "final" view, typically shown at the end of an experiment or session.

    This view displays the participant's final score and, optionally, their rank or performance category.
    It can also present navigation elements, such as a "Play again" button or links to other parts of the site.
    Branding elements like a logo or social sharing options can be included to enhance user engagement.
    A feedback section may also be provided if `feedback_info` is supplied.

    The returned data aligns with `FinalActionDto`, ensuring type consistency and making the structure
    clear for both developers and documentation readers. It can be consumed by a frontend component
    (e.g.,
    [Final.tsx](https://amsterdam-music-lab.github.io/MUSCLE/storybook/?path=/story/final--default)) to render the final screen.

    Args:
        session (Session): The current session object associated with the participant.
        title (str): The title displayed at the top of the final view. Defaults to a localized "Final score".
        final_text (str): An optional concluding message (e.g., "Thanks for participating!").
        button (ButtonDto): Optional call-to-action button configuration. For example:
                            {"text": "Play again", "link": "/{experiment_slug}"}.
        points (str): The label for the score units (e.g., "points"). Defaults to a localized "points".
        rank (str): The participant's rank (e.g., "GOLD"). If not provided, no rank is displayed.
        show_profile_link (bool): If True, display a link to the participant's profile.
        show_participant_link (bool): If True, display a participant-related link or information.
        show_participant_id_only (bool): If True, only the participant ID is shown, without a link.
        feedback_info (dict): Optional dictionary containing feedback-related data. For example:
                              {"header": "Feedback", "prompt": "Tell us what you think", "button_text": "Submit"}.
        total_score (float): Explicit final score. If None, this is derived from the session.
        logo (LogoDto): Optional logo configuration for branding. For example:
                        {"image": "/static/logo.png", "link": "https://example.com"}.

    Attributes:
        session (Session): The session object for the current participant.
        title (str): The title for the final view.
        final_text (str): A concluding message for the participant.
        button (ButtonDto): Configuration for an optional CTA button.
        rank (str): The participant's performance rank.
        show_profile_link (bool): Whether to show a profile link.
        show_participant_link (bool): Whether to show participant-related data.
        show_participant_id_only (bool): Whether only to display the participant ID.
        feedback_info (dict): Information for a feedback section.
        logo (LogoDto): Configuration for a logo displayed in the final view.
        total_score (float): The participant’s final score.
        points (str): Label for the scoring unit.

    Note:
        The `action()` method returns a `FinalActionDto` that can be consumed by the frontend
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
        final_text: str | None = None,
        button: ButtonDto | None = None,
        points: str | None = None,
        rank: str | None = None,
        show_profile_link: bool = False,
        show_participant_link: bool = False,
        show_participant_id_only: bool = False,
        feedback_info: dict | None = None,
        total_score: float | None = None,
        logo: LogoDto | None = None,
    ):
        """
        Initialize the final action data.

        Args:
            session (Session): The current participant's session.
            title (str, optional): The final view's title. Defaults to "Final score".
            final_text (str, optional): Concluding message text. Defaults to None.
            button (ButtonDto, optional): CTA button configuration. Defaults to None.
            points (str, optional): Label for points. Defaults to "points".
            rank (str, optional): Participant's rank (e.g., 'GOLD'). Defaults to None.
            show_profile_link (bool, optional): Show profile link if True. Defaults to False.
            show_participant_link (bool, optional): Show participant data link if True. Defaults to False.
            show_participant_id_only (bool, optional): Show only participant ID if True. Defaults to False.
            feedback_info (dict, optional): Feedback data. Defaults to None.
            total_score (float, optional): Explicit score. If None, derived from session. Defaults to None.
            logo (LogoDto, optional): Logo configuration. Defaults to None.
        """
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

    def action(self) -> FinalActionDto:
        """
        Get the final action data for rendering the final view.

        Returns:
            FinalActionDto: The final action data serialized for the client.
        """
        return {
            "view": self.ID,
            "score": self.total_score,
            "rank": self.rank,
            "final_text": self.final_text,
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

    def get_social_media_config(self, session: Session) -> SocialMediaConfigDto | None:
        """
        Retrieve social media configuration related to the experiment.

        Args:
            session (Session): The current participant's session object.

        Returns:
            SocialMediaConfigDto | None: Social media configuration for sharing results.
            Returns None if no configuration is available.
        """
        experiment = session.block.phase.experiment
        if hasattr(experiment, "social_media_config") and experiment.social_media_config:
            return serialize_social_media_config(experiment.social_media_config, session.total_score())
