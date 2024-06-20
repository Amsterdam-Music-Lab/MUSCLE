import random

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from experiment.actions import Consent, Explainer, Final, Playlist, Step, Trial
from experiment.actions.playback import VisualMatchingPairs
from question.demographics import EXTRA_DEMOGRAPHICS
from question.utils import question_by_key
from result.utils import prepare_result

from section.models import Section


class VisualMatchingPairsGame(Base):
    ID = 'VISUAL_MATCHING_PAIRS'
    num_pairs = 8
    contact_email = 'aml.tunetwins@gmail.com'

    def __init__(self):
        self.question_series = [
            {
                "name": "Demographics",
                "keys": [
                    'dgf_gender_identity',
                    'dgf_generation',
                    'dgf_musical_experience',
                    'dgf_country_of_origin',
                    'dgf_education_matching_pairs',
                ],
                "randomize": False
            },
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
                    'link': self.get_play_again_url(session)
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

        playback = VisualMatchingPairs(
            sections=player_sections
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
