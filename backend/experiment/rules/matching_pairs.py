import random

from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.actions import Consent, Explainer, Final, Playlist, Score, StartSession, Step, Trial
from experiment.actions.form import BooleanQuestion, Form
from experiment.actions.playback import Playback
from experiment.actions.utils import combine_actions
from result.utils import prepare_result

class MatchingPairs(Base):
    ID = 'MATCHING_PAIRS'

    @classmethod
    def first_round(cls, experiment, participant):
        consent = Consent.action()
        # 3. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 4. Start session.
        start_session = StartSession.action()

        return [
            consent,
            playlist,
            start_session
        ]
    
    @staticmethod
    def next_round(session):
        if session.result_set.count() == 0:
            explainer = Explainer(
                instruction=_('You are about to play a memory game. On the next page you will see 12 different cards. Your task is to try to find pairs of similar music.'),
                steps=[
                    Step(description=_('On each turn, you can select two cards.')),
                    Step(description=_('If the two cards you pick match, you will be awarded some points.')),
                    Step(description=_('Once you find a match, we will clear those cards from the board!')),
                    Step(description=_('If you are not able to find a match, you can try again.')),
                    Step(description=_('Try to get as high a score as possible!'))
                ]
            ).action(step_numbers=True)
            trial = MatchingPairs.get_matching_pairs_trial(session)
            return [explainer, trial]
            
        last_result = session.result_set.last()
        if last_result.question_key == 'play_again':
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
            cont = Trial(
                playback=None,
                feedback_form=Form([BooleanQuestion(
                    key='play_again',
                    question='Do you want to play again?',
                    result_id=prepare_result(session),
                    submits=True),
                ])
            ).action()
            return combine_actions(score, cont)

    @classmethod
    def get_matching_pairs_trial(cls, session):
        sections = list(session.playlist.section_set.all())
        player_sections = random.sample(sections, 2)*2
        random.shuffle(player_sections)
        playback = Playback(
            sections=player_sections,
            player_type='MULTIPLAYER',
        )
        trial = Trial(
            title='Matching pairs',
            playback=playback,
            feedback_form=None,
            result_id=prepare_result(session, question_key='matching_pairs'),
            config={'show_continue_button': False}
        )
        return trial.action()


    @classmethod
    def calculate_score(cls, result, data):
        if result.question_key == 'play_again':
            score = 1 if data.get('value') == 'yes' else 0
        else:
            moves = data.get('moves')
            score = round(sum([int(m['score']) for m in moves if m['score']>=0]) / len(moves) * 100)
        return score
