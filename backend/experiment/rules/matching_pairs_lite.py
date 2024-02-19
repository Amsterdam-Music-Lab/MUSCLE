import random
import json

from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.actions import Final, Playlist, Trial, Info
from experiment.actions.playback import MatchingPairs
from result.utils import prepare_result

from section.models import Section


class MatchingPairsLite(Base):
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
            social_info = self.social_media_info(session.experiment, session.final_score)
            social_info['apps'].append('clipboard')
            score = Final(
                session,
                title='Score',
                final_text='Can you score higher than your friends and family? Share and let them try!',
                button={
                    'text': 'Play again',
                },
                rank=self.rank(session, exclude_unfinished=False),
                social=social_info,
                feedback_info=self.feedback_info()
            )
            cont = self.get_matching_pairs_trial(session)
            return [score, cont]

    def get_matching_pairs_trial(self, session):
        json_data = session.load_json_data()
        pairs = json_data.get('pairs', [])
        if len(pairs) < self.num_pairs:
            pairs = list(session.playlist.section_set.order_by().distinct('group').values_list('group', flat=True))
            random.shuffle(pairs)
        selected_pairs = pairs[:self.num_pairs]
        session.save_json_data({'pairs': pairs[self.num_pairs:]})
        originals = session.playlist.section_set.filter(group__in=selected_pairs, tag='Original')  
        degradations = json_data.get('degradations')
        if not degradations:
            degradations = ['Original', '1stDegradation', '2ndDegradation']
            random.shuffle(degradations)
        degradation_type = degradations.pop()
        session.save_json_data({'degradations': degradations})
        if degradation_type == 'Original':
            player_sections = player_sections = list(originals) * 2
        else:
            degradations = session.playlist.section_set.filter(group__in=selected_pairs, tag=degradation_type)
            player_sections = list(originals) + list(degradations)
        random.shuffle(player_sections)
        playback = MatchingPairs(
            sections=player_sections,
            stop_audio_after=5,
            show_animation=self.show_animation,
            score_feedback_display=self.score_feedback_display,
        )
        trial = Trial(
            title='Tune twins',
            playback=playback,
            feedback_form=None,
            config={'show_continue_button': False}
        )
        return trial

    def calculate_score(self, result, data):
        ''' not used in this experiment '''
        pass
    
    def calculate_intermediate_score(self, session, result):
        ''' will be called every time two cards have been turned '''
        result_data = json.loads(result)
        first_card = result_data['lastCard']
        first_section = Section.objects.get(pk=first_card['id'])
        first_card['filename'] = str(first_section.filename)
        second_card = result_data['currentCard']
        second_section = Section.objects.get(pk=second_card['id'])
        second_card['filename'] = str(second_section.filename)
        if first_section.group == second_section.group:
            if 'seen' in second_card:
                score = 20
                given_response = 'match'
            else:
                score = 10
                given_response = 'lucky match'
        else:
            if 'seen' in second_card:
                score = -10
                given_response = 'misremembered'
            else:
                score = 0
                given_response = 'no match'
        prepare_result('move', session, json_data=result_data,
                       score=score, given_response=given_response)
        return score

        
