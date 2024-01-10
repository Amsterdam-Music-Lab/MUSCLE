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


class VisualMatchingPairs(Base):
    ID = 'VISUAL_MATCHING_PAIRS'
    num_pairs = 8
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
                trial = self.get_visual_matching_pairs_trial(session)
                return [trial]
        else:
            session.final_score += session.result_set.filter(
                question_key='visual_matching_pairs').last().score
            session.save()
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
            cont = self.get_visual_matching_pairs_trial(session)
            return [score, cont]
    
    def get_visual_matching_pairs_trial(self, session):

        player_sections = list(session.playlist.section_set.filter(tag__contains='vmp'))
        random.shuffle(player_sections)

        playback = Playback(
            sections=player_sections,
            player_type='VISUALMATCHINGPAIRS',
            play_config={ 'play_method': 'PREFETCH' }
        )
        trial = Trial(
            title='Visual Tune twins',
            playback=playback,
            feedback_form=None,
            result_id=prepare_result('visual_matching_pairs', session),
            config={'show_continue_button': False}
        )
        return trial

    def calculate_score(self, result, data):
        moves = data.get('result').get('moves')
        for m in moves:
            m['filename'] = str(Section.objects.get(pk=m.get('selectedSection')).filename)
        score = data.get('result').get('score')
        return score