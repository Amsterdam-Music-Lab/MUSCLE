"""
Setup block data in the admin panel

* Choose a slug for the block ('tafc')

* Upload sound files
    * Find the root directory name of the uploaded sound files. It is backend/upload on your local machine. On a server, ask the administrator.
    * Create a new directory within the root directory, use slug 'tafc' for the name
    * Copy files (sample_1.wav - sample_5.wav)

* Create playlist:
    * Playlists -> Add
    * Name: tafc
    * Process CSV: yes
    * CSV (see format explanation at the bottom of text entry field):
        Sample Artist 1,Sample Song 1,0.0,1.25,tafc/sample_1.wav,A,CRV
        Sample Artist 2,Sample Song 2,0.0,1.25,tafc/sample_2.wav,B,MTW
        Sample Artist 3,Sample Song 3,0.0,1.25,tafc/sample_3.wav,A,CRV
        Sample Artist 4,Sample Song 4,0.0,1.25,tafc/sample_4.wav,A,GWN
        Sample Artist 5,Sample Song 5,0.0,1.25,tafc/sample_5.wav,B,CGB
    * Save

* Create experiment
    * Admin panel -> Blocks -> Add
    * Choose name: TwoAlternativeForced
    * Slug: tafc
    * Rules: TwoAlternativeForced
    * Rounds: 5
    * Playlists: tafc
    * Save and continue editing
    * QUESTION SERIES -> Add rules' default and save
"""

from .base import BaseRules
from experiment.actions import Explainer, Trial, Final
from experiment.actions.playback import PlayButton
from experiment.actions.styles import ButtonStyle, ColorScheme, TextStyle
from django.db.models import Avg
from experiment.actions.form import Form, ChoiceQuestion
from result.utils import prepare_result


class TwoAlternativeForced(BaseRules):
    # Add to __init.py__ file in the same directory as the current file:
    #    from .tafc import TwoAlternativeForced
    # To BLOCK_RULES dictionary in __init.py__
    #    TwoAlternativeForced.ID: TwoAlternativeForced
    ID = 'TWO_ALTERNATIVE_FORCED'

    def __init__(self):
        # Create questionaire to ask for age, gender, native language and musical experience. It will be run after a session is created.
        self.question_series = [{
            "name": "EXTRA_DEMOGRAPHICS",
            "keys": ['dgf_age', 'dgf_gender_reduced', 'dgf_native_language', 'dgf_musical_experience'],
            "randomize": False
        }]

    def get_intro_explainer(self) -> Explainer:
        """
        Returns an introductory explanation of the experiment.
        """
        return Explainer(
            instruction="This is a listening experiment in which you have to respond to short sound sequences",
            steps=[],
            button_label='Ok'
        )

    def next_round(self, session):
        """
        Returns a list of actions.
        Actions used here: Final, Trial (returned by get_open_questions(), next_trial_action()), Explainer (also returned by get_feedback())
        """

        # get_open_questions() returns questions that haven't been asked yet
        actions = self.get_open_questions(session)
        if actions:
            return actions

        if session.get_rounds_passed() == 0:
            # Beginning of experiment, return an explainer and the next trial action, no feedback on previous trial
            return [self.get_intro_explainer(), self.next_trial_action(session)]

        elif not session.rounds_complete():
            # Combine two actions, feedback on previous action and next trial action
            return [self.get_feedback(session), self.next_trial_action(session)]

        else:
            # All sections have been played, finalize the experiment and return feedback
            session.finish()
            session.save()

            return [self.get_feedback(session), self.get_final_view(session)]

    def next_trial_action(self, session):
        """
        Returns the next trial action for the experiment. Not necessary as a separate method, but often used for convenience.
        An existing function experiment.actions.wrappers.two_alternative_forced() could be used to simplify the steps below
        """

        # Retrieve next section in the sequence
        section = session.playlist.section_set.all()[session.get_rounds_passed()]

        # Determine expected response, in this case section tag (A or B)
        expected_response = section.tag

        # Build Trial action, configure through config argument. Trial has Playback and Form with ChoiceQuestion to submit response.

        playback = PlayButton([section])

        key = 'choice'
        button_style = [
            ColorScheme.NEUTRAL,
            TextStyle.INVISIBLE,
            ButtonStyle.LARGE_GAP,
            ButtonStyle.LARGE_TEXT,
        ]
        question = ChoiceQuestion(
            key=key,
            result_id=prepare_result(
                key,
                session=session,
                section=section,
                expected_response=expected_response,
                scoring_rule='CORRECTNESS',
            ),
            question="A or B?",
            choices={
                'A': 'Answer A',
                'B': 'Answer B'
            },
            view='BUTTON_ARRAY',
            submits=True,
            style=button_style
        )

        feedback_form = Form([question])

        trial = Trial(
            playback=playback,
            feedback_form=feedback_form,
            title=f"Round {session.get_rounds_passed()} / {len(session.playlist.section_set.all())}",
            config = {'listen_first': True, 'decision_time': section.duration + .1}
        )

        return trial

    def get_feedback(self, session):
        """
        Get feedback for the previous trial. Not necessary as a separate method.
        """

        instruction = 'Your response was CORRECT' if session.last_result().given_response == session.last_result().section.tag else 'Your response was INCORRECT'
        button_label='Next fragment' if not session.rounds_complete() else 'Show final score'
        feedback =  Explainer(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )

        return feedback

    def get_final_view(self, session):
        """
        Get Final view (action).
        """

        # Calculate average score
        score_avg = session.result_set.all().aggregate(Avg('score'))['score__avg']
        score_percent = score_avg * 100

        # Assign rank based on percentage of correct responses
        ranks = Final.RANKS
        if score_percent == 100:
            rank = ranks['PLATINUM']
            final_text = "Congratulations! You did great and won a platinum medal!"
        elif score_percent >= 80:
            rank = ranks['GOLD']
            final_text = "Congratulations! You did great and won a gold medal!"
        elif score_percent >= 60:
            rank = ranks['SILVER']
            final_text = "Congratulations! You did very well and won a silver medal!"
        elif score_percent >= 40:
            rank = ranks['BRONZE']
            final_text = "Congratulations! You did well and won a bronze medal!"
        else:
            rank = ranks['PLASTIC']
            final_text = "Congratulations! You did OK and won a plastic medal!"

        final = Final(
            session=session,
            final_text=final_text,
            rank=rank,
            total_score=round(score_percent),
            points='% correct'
        )

        return final
