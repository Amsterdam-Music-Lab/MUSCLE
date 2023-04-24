import random

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from experiment.actions import Consent, Explainer, Final, Playlist, Score, StartSession, Step, Trial
from experiment.actions.form import BooleanQuestion, Form
from experiment.actions.playback import Playback
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.utils import question_by_key, unasked_question
from result.utils import prepare_result

class MatchingPairs(Base):
    ID = 'MATCHING_PAIRS'

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
                Step(description=_('You are invited to play a memory game.')),
                Step(description=_('The more similar pairs you find, the more points you receive.')),
                Step(description=_('Try to get as many points as possible!'))
            ]).action(step_numbers=True)

        return [
            consent,
            playlist,
            explainer,
            start_session
        ]
    
    @staticmethod
    def next_round(session):
        if session.rounds_passed() <= 1:       
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
            
        last_result = session.result_set.last()
        if last_result and last_result.question_key == 'play_again':
            if last_result.score == 1:
                return MatchingPairs.get_matching_pairs_trial(session)
            else:
                session.finish()
                session.save()
                return Final(
                    session=session,
                    final_text='Thank you for playing!',
                    show_social=False,
                    show_profile_link=True
                ).action()
        else:
            session.final_score += session.result_set.filter(
                question_key='matching_pairs').last().score
            session.save()
            score = Score(
                session,
                config={'show_total_score': True},
                title='Score'
            ).action()
            key = 'play_again'
            cont = Trial(
                playback=None,
                feedback_form=Form([BooleanQuestion(
                    key=key,
                    question='Play again?',
                    result_id=prepare_result(key, session),
                    submits=True),
                ])
            ).action()
            return [score, cont]
    
    @classmethod
    def get_question(cls, session):
        questions = [
            question_by_key('dgf_gender_identity'),
            question_by_key('dgf_generation'),
            question_by_key('dgf_musical_experience', EXTRA_DEMOGRAPHICS)
        ]
        question = unasked_question(session.participant, questions)
        if not question:
            return None, None
        skip_explainer = session.load_json_data().get('explainer_shown')
        if not skip_explainer:
            session.save_json_data({'explainer_shown': True})
        return Trial(
            title=_("Questionnaire"),
            feedback_form=Form([question])
        ).action(), skip_explainer

    @classmethod
    def get_matching_pairs_trial(cls, session):
        sections = list(session.playlist.section_set.all())
        player_sections = random.sample(sections, 6)*2
        random.shuffle(player_sections)
        playback = Playback(
            sections=player_sections,
            player_type='MATCHINGPAIRS',
            play_config={'stop_audio_after': 4}
        )
        trial = Trial(
            title='Matching pairs',
            playback=playback,
            feedback_form=None,
            result_id=prepare_result('matching_pairs', session),
            config={'show_continue_button': False}
        )
        return trial.action()

    @classmethod
    def calculate_score(cls, result, data):
        if result.question_key == 'play_again':
            score = 1 if data.get('value') == 'yes' else 0
        elif result.question_key == 'matching_pairs':
            moves = data.get('moves')
            score = sum([int(m['score']) for m in moves if 
                               m.get('score') and m['score']!= None]) + 100
        else:
            score = 0
        return score
