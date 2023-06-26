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
    num_pairs = 2

    @classmethod
    def feedback_info(cls):
        pass

    @classmethod
    def first_round(cls, experiment):
        rendered = render_to_string('consent/consent_rhythm.html')
        consent = Consent.action(rendered, title=_(
            'Informed consent'), confirm=_('I agree'), deny=_('Stop'))
        # 2. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 3. Start session.
        start_session = StartSession.action()

        explainer = Explainer(
            instruction='',
            steps=[
                Step(description=_('On the next page, you will find a board with 16 music cards.')),
                Step(description=_('Two cards are tune twins, but one sound may be distorted.')),
                Step(description=_('Your task is to find all the tune twins on the board.'))
            ]).action(step_numbers=True)

        return [
            consent,
            playlist,
            explainer,
            start_session
        ]
    
    @staticmethod
    def next_round(session):
        if session.rounds_passed() < 1:       
            trial, skip_explainer = MatchingPairs.get_question(session)
            if trial:
                if not skip_explainer:
                    intro_questions = Explainer(
                        instruction='Before starting the game, we would like to ask you some demographic questions.',
                        steps=[]
                    ).action()
                    return [intro_questions, trial]
            else:
                trial = MatchingPairs.get_matching_pairs_trial(session)
            return trial
        else:
            session.final_score += session.result_set.filter(
                question_key='matching_pairs').last().score
            session.save()
            score = Final(
                session,
                title='Score',
                final_text='Can you score higher than your friends and family? Share and let them try!',
                button={
                    'text': 'Play again',
                },
                rank=MatchingPairs.rank(session, exclude_unfinished=False),
                show_social=True,
            ).action()
            cont = MatchingPairs.get_matching_pairs_trial(session)
            return [score, cont]
    
    @classmethod
    def get_question(cls, session):
        questions = [
            question_by_key('dgf_gender_identity'),
            question_by_key('dgf_generation'),
            question_by_key('dgf_musical_experience', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_country_of_origin'),
            question_by_key('dgf_education')
        ]
        open_questions = total_unanswered_questions(session.participant, questions)
        if not open_questions:
            return None, None
        total_questions = int(session.load_json_data().get('saved_total', '0'))
        if not total_questions:
            total_questions = open_questions     
            session.save_json_data({'saved_total': open_questions})
        question = unasked_question(session.participant, questions)
        skip_explainer = session.load_json_data().get('explainer_shown')
        if not skip_explainer:
            session.save_json_data({'explainer_shown': True})
        index = total_questions - open_questions + 1
        return Trial(
            title=_("Questionnaire %(index)i / %(total)i") % {'index': index, 'total': total_questions},
            feedback_form=Form([question])
        ).action(), skip_explainer

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
        return trial.action()

    @classmethod
    def calculate_score(cls, result, data):
        moves = data.get('result').get('moves')
        for m in moves:
            m['filename'] = str(Section.objects.get(pk=m.get('selectedSection')).filename)
        score = sum([int(m['score']) for m in moves if 
                           m.get('score') and m['score']!= None]) + 100
        return score
