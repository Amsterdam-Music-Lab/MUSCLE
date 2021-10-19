class Final:  # pylint: disable=too-few-public-methods
    """
    Provide data for a final view

    Relates to client component: Final.js    
    """

    ID = 'FINAL'

    @staticmethod
    def action(session, title, score_message=None):
        """Get data for final_score action"""
        return {
            'view': Final.ID,
            'score': session.total_score(),
            'score_message': score_message,
            'title': title
        }
