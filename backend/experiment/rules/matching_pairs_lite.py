from django.utils.translation import gettext_lazy as _

from .matching_pairs import MatchingPairsGame
from experiment.actions import Final, Playlist, Info


class MatchingPairsLite(MatchingPairsGame):
    ID = 'MATCHING_PAIRS_LITE'
    num_pairs = 8
    show_animation = False
    score_feedback_display = 'small-bottom-right'
    contact_email = 'aml.tunetwins@gmail.com'

    def first_round(self, experiment):     
        # 2. Choose playlist.
        playlist = Playlist(experiment.playlists.all())
        info = Info('',
                    heading='Press start to enter the game',
                    button_label='Start')
        return [
            playlist, info
        ]
    
    def next_round(self, session):
        if session.rounds_passed() < 1:
            trial = self.get_matching_pairs_trial(session)
            return [trial]
        else:
            # final score saves the result from the cleared board into account
            score = Final(
                session,
                title='Score',
                final_text='End of the game',
                button={
                    'text': 'Back to dashboard',
                },
            )
            return score
