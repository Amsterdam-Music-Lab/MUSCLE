import random

from django.utils.translation import gettext_lazy as _

from .matching_pairs import MatchingPairsGame
from experiment.actions import Final, Playlist, Info
from experiment.actions.utils import COLLECTION_KEY


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
    
    def next_round(self, session, request_session=None):
        if session.rounds_passed() < 1:
            trial = self.get_matching_pairs_trial(session)
            return [trial]
        else:
            print(request_session.keys())
            # final score saves the result from the cleared board into account
            score = Final(
                session,
                title='Score',
                final_text='End of the game',
                button={
                    'text': 'Back to dashboard', 'link': '/collection/{}'.format(request_session.get(COLLECTION_KEY))
                },
            )
            return score

    def select_sections(self, session):
        pairs = list(session.playlist.section_set.order_by().distinct(
            'group').values_list('group', flat=True))
        random.shuffle(pairs)
        selected_pairs = pairs[:self.num_pairs]
        originals = session.playlist.section_set.filter(
            group__in=selected_pairs, tag='Original')
        degradations = session.playlist.section_set.filter(
            group__in=selected_pairs, tag='Degradation')
        if degradations:
            player_sections = list(originals) + list(degradations)
        else:
            player_sections = list(originals) + list(originals)
        return player_sections
