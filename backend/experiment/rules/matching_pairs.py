import random
import json

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from experiment.actions import Consent, Explainer, Final, Playlist, Step, Trial
from experiment.actions.playback import MatchingPairs
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.utils import question_by_key
from result.utils import prepare_result

from section.models import Section


class MatchingPairsGame(Base):
    ID = 'MATCHING_PAIRS'
    num_pairs = 8
    show_animation = True
    score_feedback_display = 'large-top'
    contact_email = 'aml.tunetwins@gmail.com'

    def __init__(self):
        self.questions = [
            question_by_key('dgf_gender_identity'),
            question_by_key('dgf_generation'),
            question_by_key('dgf_musical_experience', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_country_of_origin'),
            question_by_key('dgf_education', drop_choices=['isced-2', 'isced-5'])
        ]

    def first_round(self, experiment):
        # Add consent from file or admin (admin has priority)
        consent = Consent(
            experiment.consent,
            title=_('Informed consent'),
            confirm=_('I agree'),
            deny=_('Stop'),
            url='consent/consent_matching_pairs.html'
            )
        # 2. Choose playlist.
        playlist = Playlist(experiment.playlists.all())

        explainer = Explainer(
            instruction='',
            steps=[
                Step(description=_('TuneTwins is a musical version of "Memory". It consists of 16 musical fragments. Your task is to listen and find the 8 matching pairs.')),
                Step(description=_('Some versions of the game are easy and you will have to listen for identical pairs. Some versions are more difficult and you will have to listen for similar pairs, one of which is distorted.')),
                Step(description=_('Click on another card to stop the current card from playing.')),
                Step(description=_('Finding a match removes the pair from the board.')),
                Step(description=_('Listen carefully to avoid mistakes and earn more points.'))
            ],
            step_numbers=True)

        return [
            consent,
            playlist,
            explainer
        ]
    
    def next_round(self, session):
        if session.rounds_passed() < 1:
            trials = self.get_questionnaire(session)
            if trials:
                intro_questions = Explainer(
                    instruction=_('Before starting the game, we would like to ask you %i demographic questions.' % (len(trials))),
                    steps=[]
                )
                return [intro_questions, *trials]
            else:
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

        
