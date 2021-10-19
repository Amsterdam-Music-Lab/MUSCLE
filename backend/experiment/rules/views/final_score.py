from django.utils.translation import gettext_lazy as _

class FinalScore:  # pylint: disable=too-few-public-methods
    """
    Provide data for a final score view

    Relates to client component: FinalScore.js
    """

    ID = 'FINAL_SCORE'

    # rankstyles available in client::FinalScore.scss
    RANKS = {
        'PLASTIC': {'text': _('plastic'), 'class': 'plastic'},
        'BRONZE':  {'text': _('bronze'), 'class': 'bronze'},
        'SILVER': {'text': _('silver'), 'class': 'silver'},
        'GOLD': {'text': _('gold'), 'class': 'gold'},
        'PLATINUM': {'text': _('platinum'), 'class': 'platinum'},
        'DIAMOND': {'text': _('diamond'), 'class': 'diamond'}
    }

    @staticmethod
    def action(session, score_message, rank, show_social=True):
        """Get data for final_score action"""
        return {
            'view': FinalScore.ID,
            'score': session.final_score,
            'rank': rank,
            'score_message': score_message,
            'points': _("points"),
            'action_texts': {
                'play_again': _('Play again'),
                'profile': _('My profile'),
                'all_experiments': _('All experiments')
            },
            'title': _("Final score"),
            'show_social': show_social
        }
