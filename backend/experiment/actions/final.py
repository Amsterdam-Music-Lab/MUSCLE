from django.utils.translation import gettext_lazy as _

from experiment.serializers import serialize_social_media_config
from session.models import Session

from .base_action import BaseAction


class Final(BaseAction):  # pylint: disable=too-few-public-methods
    """
    Provide data for a final view

    Relates to client component: Final.js
    """

    ID = 'FINAL'

    RANKS = {
        'PLASTIC': {'text': _('plastic'), 'class': 'plastic'},
        'BRONZE':  {'text': _('bronze'), 'class': 'bronze'},
        'SILVER': {'text': _('silver'), 'class': 'silver'},
        'GOLD': {'text': _('gold'), 'class': 'gold'},
        'PLATINUM': {'text': _('platinum'), 'class': 'platinum'},
        'DIAMOND': {'text': _('diamond'), 'class': 'diamond'}
    }

    def __init__(
        self,
        session: Session,
        title: str = _("Final score"),
        final_text: str = None,
        button: dict = None,
        points: str = None,
        rank: str = None,
        show_profile_link: bool = False,
        show_participant_link: bool = False,
        show_participant_id_only: bool = False,
        feedback_info: dict = None,
        total_score: float = None,
        logo: dict = None,
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

    def action(self):
        """Get data for final action"""
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

    def get_social_media_config(self, session: Session) -> dict:
        experiment = session.block.phase.experiment
        if (
            hasattr(experiment, "social_media_config")
            and experiment.social_media_config
        ):
            return serialize_social_media_config(
                experiment.social_media_config, session.total_score()
            )
