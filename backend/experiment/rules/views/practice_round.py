
class PracticeRound:  # pylint: disable=too-few-public-methods
    """
    Provide data for a PracticeSession view that plays a section, shows a question and has yes/no buttons

    Relates to client component: PracticeRound.js    
    """

    ID = 'PRACTICE_ROUND'

    @staticmethod
    def action(section, instruction, title='Practice'):
        """Get data for song_bool action"""

        # Create action
        action = {
            'view': PracticeRound.ID,
            'title': title,
            'instruction': instruction
        }

        # Section
        action['section'] = {
            'id': section.id,
            'artist': section.artist,
            'song': section.name,
            'url': section.absolute_url(),
        }

        # Config
        action['config'] = {
            'ready_time': 0,
            'decision_time': 15
        }

        return action
