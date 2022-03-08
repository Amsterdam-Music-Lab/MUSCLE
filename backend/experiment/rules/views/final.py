from django.utils.translation import gettext as _

class Final:  # pylint: disable=too-few-public-methods
    """
    Provide data for a final view

    Relates to client component: Final.js    
    """

    ID = 'FINAL'

    @staticmethod
    def action(session, title, score_template=None, button=None, rank=None, show_social=False, show_profile=False, show_participant_link=False):
        """Get data for final action"""
        return {
            'view': Final.ID,
            'score': session.total_score(),
            'rank': rank,
            'score_template': score_template,
            'points': _("points"),
            'action_texts': {
                'play_again': _('Play again'),
                'profile': _('My profile'),
                'all_experiments': _('All experiments')
            },
            'title': _("Final score"),
            'show_social': show_social,
            'show_profile': show_profile,
            'show_participant_link': show_participant_link
        }
