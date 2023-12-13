from django.utils.translation import gettext_lazy as _

from experiment.actions import Consent, Explainer, Final, Playlist, StartSession, Step, Trial
from .matching_pairs import MatchingPairs

class MatchingPairsTutorial(MatchingPairs):
    ID = 'MATCHING_PAIRS_TUTORIAL'
    num_pairs = 3

    def __init__(self):
        self.questions = [
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
                    instruction=_('Log %i demographic questions:' % (len(trials))),
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
            score = Final(
                session,
                title='',
                final_text='',
                button={
                    'text': 'Play again?',
                }
            )
            cont = self.get_matching_pairs_trial(session)
            return [score, cont]

