import random

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from experiment.actions import Consent, Explainer, Final, Playlist, StartSession, Step, Trial
from experiment.actions.playback import Playback
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.utils import question_by_key
from result.utils import prepare_result

from section.models import Section

class MatchingPairsTutorial(Base):
    ID = 'MATCHING_PAIRS_TUTORIAL'
    num_pairs = 3
    contact_email = 'aml.tunetwins@gmail.com'

    def __init__(self):
        self.questions = [
            #question_by_key('dgf_gender_identity'),
            #question_by_key('dgf_generation'),
            #question_by_key('dgf_musical_experience', EXTRA_DEMOGRAPHICS),
            #question_by_key('dgf_country_of_origin'),
            #question_by_key('dgf_education', drop_choices=['isced-2', 'isced-5'])
        ]

    def first_round(self, experiment):
        # 1. Consent Removed (not needed to teach game)

        # 2. Choose playlist.
        playlist = Playlist(experiment.playlists.all())

        # 3. Start session.
        start_session = StartSession()

        explainer = Explainer(
            instruction='',
            steps=[
                Step(description=_('You are about to start the Matching Pairs Tutorial'))
            ],
            step_numbers=False)

        return [
            playlist,
            explainer,
            start_session
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
            session.final_score += session.result_set.filter(
                question_key='matching_pairs').last().score
            session.save()
            social_info = self.social_media_info(session.experiment, session.final_score)
            social_info['apps'].append('clipboard')
            score = Final(
                session,
                title='',
                final_text='',
                button={
                    'text': 'Play again',
                },
                #rank=self.rank(session, exclude_unfinished=False)
                #social=social_info,
                #feedback_info=self.feedback_info()
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
        playback = Playback(
            sections=player_sections,
            player_type='MATCHINGPAIRS',
            play_config={'stop_audio_after': 5}
        )
        trial = Trial(
            title='Tune twins',
            playback=playback,
            feedback_form=None,
            result_id=prepare_result('matching_pairs', session),
            config={'show_continue_button': False}
        )
        return trial

    def calculate_score(self, result, data):
        moves = data.get('result').get('moves')
        for m in moves:
            m['filename'] = str(Section.objects.get(pk=m.get('selectedSection')).filename)
        score = data.get('result').get('score')
        return score
