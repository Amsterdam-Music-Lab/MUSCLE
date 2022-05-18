from django.utils.translation import gettext as _

class Final:  # pylint: disable=too-few-public-methods
    """
    Provide data for a final view

    Relates to client component: Final.js
    """

    ID = 'FINAL'

    @staticmethod
    def action(session, title=_("Final score"), final_text=None, button=None, rank=None,
        show_social=False, show_profile_link=False, show_participant_link=False):
        """Get data for final action"""
        return {
            'view': Final.ID,
            'score': session.total_score(),
            'rank': rank,
            'final_text': final_text,
            'button': button,
            'points': _("points"),
            'action_texts': {
                'play_again': _('Play again'),
                'profile': _('My profile'),
                'all_experiments': _('All experiments')
            },
            'title': title,
            'show_social': show_social,
            'show_profile_link': show_profile_link,
            'show_participant_link': show_participant_link
        }
