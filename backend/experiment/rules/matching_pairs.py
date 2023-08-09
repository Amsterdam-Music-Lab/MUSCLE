import random

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings

from .base import Base
from experiment.actions import Consent, Explainer, Final, Playlist, StartSession, Step, Trial
from experiment.actions.form import Form
from experiment.actions.playback import Playback
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.utils import question_by_key, total_unanswered_questions, unasked_question
from result.utils import prepare_result

from section.models import Section

class MatchingPairs(Base):
    ID = 'MATCHING_PAIRS'
    num_pairs = 8
    contact_email = 'aml.tunetwins@gmail.com'

    questions = [
        question_by_key('dgf_gender_identity'),
        question_by_key('dgf_generation'),
        question_by_key('dgf_musical_experience', EXTRA_DEMOGRAPHICS),
        question_by_key('dgf_country_of_origin'),
        question_by_key('dgf_education')
    ]

    @classmethod
    def first_round(cls, experiment):
        rendered = render_to_string('consent/consent_matching_pairs.html')
        consent = Consent(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))
        # 2. Choose playlist.
        playlist = Playlist(experiment.playlists.all())

        # 3. Start session.
        start_session = StartSession()

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
            explainer,
            start_session
        ]
    
    @classmethod
    def next_round(cls, session):
        if session.rounds_passed() < 1:       
            trials = cls.get_questions_block(session)
            if trials:
                intro_questions = Explainer(
                    instruction=_('Before starting the game, we would like to ask you %i demographic questions.' % (len(trials))),
                    steps=[]
                )
                return [intro_questions, *trials]
            else:
                trial = cls.get_matching_pairs_trial(session)
                return [trial]
        else:
            session.final_score += session.result_set.filter(
                question_key='matching_pairs').last().score
            session.save()
            score = Final(
                session,
                title='Score',
                final_text='Can you score higher than your friends and family? Share and let them try!',
                socialm_hashtag='#TuneTwins',
                socialm_endtext='https://www.amsterdammusiclab.nl/blog/tunetwins',
                button={
                    'text': 'Play again',
                },
                rank=MatchingPairs.rank(session, exclude_unfinished=False),
                show_social=True,
                feedback_info=MatchingPairs.feedback_info()
            )
            cont = MatchingPairs.get_matching_pairs_trial(session)
            return [score, cont]

    @classmethod
    def get_matching_pairs_trial(cls, session):
        json_data = session.load_json_data()
        pairs = json_data.get('pairs', [])
        if len(pairs) < cls.num_pairs:
            pairs = list(session.playlist.section_set.order_by().distinct('group').values_list('group', flat=True))
            random.shuffle(pairs)
        selected_pairs = pairs[:cls.num_pairs]
        session.save_json_data({'pairs': pairs[cls.num_pairs:]})
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

    @classmethod
    def calculate_score(cls, result, data):
        moves = data.get('result').get('moves')
        for m in moves:
            m['filename'] = str(Section.objects.get(pk=m.get('selectedSection')).filename)
        score = data.get('result').get('score')
        return score
