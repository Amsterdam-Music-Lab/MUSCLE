import logging
from decimal import Decimal, ROUND_HALF_UP

from django.utils.translation import gettext_lazy as _

from .base import Base
from section.models import Section
from experiment.actions import Trial, Explainer, Step
from experiment.actions.form import ChoiceQuestion, Form
from experiment.actions.playback import Autoplay
from experiment.actions.utils import final_action_with_optional_button, render_feedback_trivia
from experiment.actions.utils import get_average_difference
from experiment.rules.util.practice import get_trial_condition_block, get_practice_views
from experiment.rules.util.staircasing import register_turnpoint
from result.utils import prepare_result
from section.models import Playlist
from session.models import Session

logger = logging.getLogger(__name__)


class DurationDiscrimination(Base):
    """
    These rules make use of the session's final_score to register turnpoints
    """
    ID = 'DURATION_DISCRIMINATION'
    condition = _('interval')
    start_diff = 400000
    max_turnpoints = 8
    catch_condition = 'EQUAL'
    block_size = 5
    section_count = 247
    increase_difficulty_multiplier = .5
    decrease_difficulty_multiplier = 1.5

    def next_round(self, session: Session):
        if session.final_score == 0:
            self.register_difficulty(session)
            # we are practicing
            actions = get_practice_views(
                session,
                self.get_intro_explainer(),
                self.staircasing_blocks,
                self.next_trial_action,
                self.get_response_explainer,
                self.get_previous_condition,
                self.get_difficulty(session))
            return actions

        else:
            # Actual trials
            action = self.staircasing_blocks(
                session, self.next_trial_action)
            return action

    def calculate_score(self, result, data):
        # a result's score is used to keep track of how many correct results were in a row
        # for catch trial, set score to 2 -> not counted for calculating turnpoints
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response and expected_response == result.given_response:
            if expected_response == 'LONGER':
                return 1
            else:
                return 2
        else:
            return 0

    def register_difficulty(self, session):
        session.save_json_data({'difficulty': self.start_diff})
        session.save()

    def get_previous_condition(self, last_result):
        return last_result.expected_response

    def get_response_explainer(self, correct, correct_response, button_label=_('Next fragment')):
        preposition = _('than') if correct_response == 'LONGER' else _('as')
        correct_response = _(
            'LONGER') if correct_response == 'LONGER' else _('EQUAL')
        if correct:
            instruction = _(
                'The second interval was %(correct_response)s %(preposition)s the first interval. Your answer was CORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        else:
            instruction = _(
                'The second interval was %(correct_response)s %(preposition)s the first interval. Your answer was INCORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        return Explainer(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )

    def next_trial_action(self, session, trial_condition, difficulty):
        """
        Provide the next trial action
        Arguments:
        - session: the session
        - trial_condition: 1 for catch trial, 0 for normal trial
        - difficulty: difficulty of the trial (translates to file name)
        """
        if trial_condition == 1:
            # catch trial
            difference = 0
        else:
            difference = difficulty
        try:
            section = session.playlist.section_set.get(song__name=difference)
        except Section.DoesNotExist:
            return None
        expected_response = 'EQUAL' if difference == 0 else 'LONGER'
        question_text = self.get_question_text()
        key = 'longer_or_equal'
        question = ChoiceQuestion(
            question=question_text,
            key=key,
            choices={
                'EQUAL': _('EQUALLY LONG'),
                'LONGER': _('LONGER')
            },
            view='BUTTON_ARRAY',
            result_id=prepare_result(key, session, section=section, expected_response=expected_response),
            submits=True
        )
        # create Result object and save expected result to database

        playback = Autoplay([section])
        form = Form([question])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('%(title)s duration discrimination') % {
                'title': self.condition},
            config={
                'listen_first': True,
                'response_time': section.duration + .1
            }
        )
        return view

    def get_question_text(self):
        return _("Is the second interval EQUALLY LONG as the first interval or LONGER?")

    def get_intro_explainer(self):
        return Explainer(
            instruction=self.get_introduction(),
            steps=[
                Step(self.get_task_explanation()),
                Step(_(
                    'During the experiment it will become more difficult to hear the difference.')),
                Step(_(
                    "Try to answer as accurately as possible, even if you're uncertain.")),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(_(
                    'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'))
            ],
            button_label='Ok',
            step_numbers=True
        )

    def get_task_explanation(self):
        return _("It's your job to decide if the second interval is EQUALLY LONG as the first interval, or LONGER.")

    def get_introduction(self):
        return _('In this test you will hear two time durations for each trial, which are marked by two tones.')

    def finalize_block(self, session):
        ''' After 8 turnpoints, finalize experiment
        Give participant feedback
        '''
        difference = get_average_difference(session, 4, self.start_diff)
        final_text = self.get_final_text(difference)
        session.finish()
        session.save()
        return final_action_with_optional_button(session, final_text)

    def get_final_text(self, difference):
        percentage = round(difference / 6000, 2)
        feedback = _(
            "Well done! You heard the difference between two intervals that \
            differed only {} percent in duration.").format(percentage)
        trivia = _("When we research timing in \
            humans, we often find that people's accuracy in this task scales: \
            for shorter durations, people can hear even smaller differences than for longer durations.")
        return render_feedback_trivia(feedback, trivia)

    def staircasing_blocks(self, session, trial_action_callback):
        """ Calculate staircasing procedure in blocks of 5 trials with one catch trial
        Arguments:
        - session: the session
        - trial_action_callback: function to build a trial action
        - optional: condition: if the explainers from duration_discrimination are reused, set condition
        """
        previous_results = session.result_set.order_by('-created_at')
        trial_condition = get_trial_condition_block(session, self.block_size)
        if not previous_results.count():
            # first trial
            difficulty = self.get_difficulty(session)
            return trial_action_callback(session, trial_condition, difficulty)
        previous_condition = previous_results.first().expected_response
        if previous_condition == self.catch_condition:
            # last trial was catch trial, don't calculate turnpoints
            # don't manipulate duration
            difficulty = self.get_difficulty(session)
            action = trial_action_callback(
                session,
                trial_condition,
                difficulty)
        else:
            if previous_results.first().score == 0:
                # the previous response was incorrect
                json_data = session.json_data
                direction = json_data.get('direction')
                last_result = previous_results.first()
                last_result.comment = 'decrease difficulty'
                last_result.save()
                if direction == 'increase':
                    # register turnpoint
                    register_turnpoint(session, last_result)
                if session.final_score == self.max_turnpoints + 1:
                    # experiment is finished, None will be replaced by final view
                    action = None
                else:
                    # register decreasing difficulty
                    session.save_json_data({'direction': 'decrease'})
                    session.save()
                    # decrease difficulty
                    difficulty = self.get_difficulty(
                        session, self.decrease_difficulty_multiplier)
                    action = trial_action_callback(
                        session,
                        trial_condition,
                        difficulty)
            else:
                # the previous response was correct - check if previous non-catch trial was 1
                if previous_results.count() > 1 and self.last_non_catch_correct(previous_results.all()):
                    # the previous two responses were correct
                    json_data = session.json_data
                    direction = json_data.get('direction')
                    last_correct_result = previous_results.first()
                    last_correct_result.comment = 'increase difficulty'
                    last_correct_result.save()
                    if direction == 'decrease':
                        # register turnpoint
                        register_turnpoint(session, last_correct_result)
                    if session.final_score == self.max_turnpoints + 1:
                        # experiment is finished, None will be replaced by final view
                        action = None
                    else:
                        # register increasing difficulty
                        session.save_json_data({'direction': 'increase'})
                        session.save()
                        # increase difficulty
                        difficulty = self.get_difficulty(
                            session, self.increase_difficulty_multiplier)
                        action = trial_action_callback(
                            session,
                            trial_condition,
                            difficulty)
                else:
                    difficulty = self.get_difficulty(session)
                    action = trial_action_callback(
                        session,
                        trial_condition,
                        difficulty)
        if not action:
            # action is None if the audio file doesn't exist
            return self.finalize_block(session)
        return action

    def get_difficulty(self, session, multiplier=1.0):
        '''
         - multiplier:
            1.5 multiplier for difference *increase*
            1 if difference should stay the same
            0.5 for difference *decrease*
        '''
        json_data = session.json_data
        difficulty = json_data.get('difficulty')
        current_difficulty = difficulty * multiplier
        session.save_json_data({'difficulty': current_difficulty})
        session.save()
        # return rounded difficulty
        # this uses the decimal module, since round() does not work entirely as expected
        return int(Decimal(str(current_difficulty)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

    def last_non_catch_correct(self, previous_results):
        """ check if previous responses (before the current one, which is correct)
        have been catch or non-catch, and if non-catch, if they were correct
        """
        n_results = len(previous_results)
        # get the previous scores and conditions, from most to least recent
        results = [previous_results[r] for r in range(1, n_results)]
        answer = False
        while results:
            result = results.pop(0)
            if result.score == 1:
                if result.comment:
                    # a comment on the second-to-last result indicates that difficulty changed there;
                    # we need to wait for another correct response before changing again
                    break
                else:
                    answer = True
                    break
            elif result.expected_response == self.catch_condition:
                continue
            else:
                break
        return answer

    def validate_playlist(self, playlist: Playlist):
        errors = []
        errors += super().validate_playlist(playlist)
        sections = playlist.section_set.all()
        if sections.count() is not self.section_count:
            errors.append("The playlist should contain 247 sections")
        try:
            numerical_song_names = [int(section.song_name()) for section in sections]
            if self.start_diff not in numerical_song_names:
                errors.append(
                    f"The file for the starting difference of {self.start_diff} is missing"
                )
        except:
            errors.append(
                "The sections should have an associated song with an integer name"
            )

        return errors
