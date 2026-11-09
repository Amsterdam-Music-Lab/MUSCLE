import logging
from decimal import Decimal, ROUND_HALF_UP

from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from section.models import Section
from experiment.actions.button import Button
from experiment.actions.playback import Autoplay, PlaybackSection
from experiment.actions.explainer import Explainer, Step
from experiment.actions.final import FinalView
from experiment.actions.form import Form
from experiment.actions.question import ButtonArrayQuestion
from experiment.actions.trial import Trial
from experiment.rules.mixins.practice import PracticeMixin
from experiment.rules.mixins.staircasing import StaircasingMixin
from result.models import Result
from result.utils import prepare_result
from section.models import Playlist
from session.models import Session

logger = logging.getLogger(__name__)


class DurationDiscrimination(BaseRules, PracticeMixin, StaircasingMixin):
    """
    These rules make use of the session's final_score to register turnpoints
    """
    ID = 'DURATION_DISCRIMINATION'
    task_description = _("Duration discrimination")
    subtask = _("Interval")
    start_diff = 400000
    max_turnpoints = 8
    first_condition = "longer"
    first_condition_i18n = _("LONGER")
    second_condition = "equal"  # second condition is 'catch' condition
    second_condition_i18n = _("EQUAL")
    n_practice_rounds_second_condition = 2
    block_size = 5
    section_count = 247
    increase_difficulty_multiplier = .5
    decrease_difficulty_multiplier = 1.5

    def next_round(self, session: Session) -> list:
        practice_finished = session.json_data.get("practice_done")
        if not practice_finished:
            # we are practicing
            return self.next_practice_round(session)

        else:
            # Actual trials
            return self.staircasing_blocks(session)

    def calculate_score(self, result: Result, data: dict) -> int:
        # a result's score is used to keep track of how many correct results were in a row
        # for catch condition, set score to 2 -> not counted for calculating turnpoints
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response and expected_response == result.given_response:
            if expected_response == self.first_condition:
                return 1
            else:
                return 2
        else:
            return 0

    def get_average_difference(
        self, session: Session, num_turnpoints: int, initial_value: int
    ) -> float:
        """
        Description: Calculate and return the average difference in milliseconds participants could hear (from the last `num_turnpoints` records).

        Args:
            session (Session): The current session.
            num_turnpoints (int): The number of last turnpoints to consider.
            initial_value (float): A fallback initial value.

        Returns:
            (float): The average difference in milliseconds.

        Example:
            ```python
            avg_diff = get_average_difference(my_session, 3, 20.0)
            ```
        """
        last_turnpoints = self.get_last_n_turnpoints(session, num_turnpoints)
        if last_turnpoints.count() == 0:
            last_result = self.get_fallback_result(session)
            if last_result:
                return float(last_result.section.song.name)
            else:
                # this cannot happen in DurationDiscrimination style blocks
                # for future compatibility, still catch the condition that there may be no results
                return initial_value
        return (
            sum([int(result.section.song.name) for result in last_turnpoints])
            / last_turnpoints.count()
        )

    def get_feedback_explainer(self, session):
        button_label = _("Next fragment")
        correct_response, is_correct = self.get_condition_and_correctness(session)
        preposition = _("than") if is_correct else _("as")
        if is_correct:
            instruction = _(
                'The second interval was %(correct_response)s %(preposition)s the first interval. Your answer was CORRECT.'
            ) % {'correct_response': correct_response, 'preposition': preposition}
        else:
            instruction = _(
                'The second interval was %(correct_response)s %(preposition)s the first interval. Your answer was INCORRECT.'
            ) % {'correct_response': correct_response, 'preposition': preposition}
        return Explainer(instruction=instruction, steps=[], button=Button(button_label))

    def get_next_trial(self, session: Session) -> Trial:
        """
        Provide the next trial action

        Args:
            session: the session
            trial_condition: string defined by second_condition for catch trial, first_condition for normal trial
            difficulty: difficulty of the trial (translates to file name)
        """
        trial_condition = self.get_condition(session)
        difficulty = self.get_difficulty(session)
        if trial_condition == self.second_condition:
            # catch trial
            difference = 0
        else:
            difference = difficulty
        try:
            section = session.playlist.section_set.get(song__name=difference)
        except Section.DoesNotExist:
            return None
        question_text = self.get_question_text()
        identifier = self.task_description.replace(" ", "_")
        question = ButtonArrayQuestion(
            text=question_text,
            identifier=identifier,
            choices=[
                {
                    'value': self.first_condition,
                    'label': self.first_condition_i18n,
                    'color': 'colorNeutral1',
                },
                {
                    'value': self.second_condition,
                    'label': self.second_condition_i18n,
                    'color': 'colorNeutral2',
                },
            ],
            result_id=prepare_result(
                identifier, session, section=section, expected_response=trial_condition
            ),
        )

        playback = Autoplay(sections=[PlaybackSection(section)], show_animation=False)
        form = Form([question], submit_button=None)
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_("%(title)s %(task)s")
            % {"title": self.subtask, "task": self.task_description},
            listen_first=True,
            response_time=section.duration + 0.1,
        )
        return view

    def get_question_text(self):
        return _("Is the second interval EQUALLY LONG as the first interval or LONGER?")

    def get_intro_explainer(self):
        return Explainer(
            instruction=self.get_introduction(),
            steps=[
                Step(self.get_task_explanation()),
                Step(
                    _(
                        'During the experiment it will become more difficult to hear the difference.'
                    )
                ),
                Step(
                    _(
                        "Try to answer as accurately as possible, even if you're uncertain."
                    )
                ),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(
                    _(
                        'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'
                    )
                ),
            ],
            button=Button('Ok'),
            step_numbers=True,
        )

    def get_task_explanation(self):
        return _(
            "It's your job to decide if the second interval is EQUALLY LONG as the first interval, or LONGER."
        )

    def get_introduction(self):
        return _(
            'In this test you will hear two time durations for each trial, which are marked by two tones.'
        )

    def get_final_statistics(self, session: Session) -> dict:
        difference = self.get_average_difference(session, 4, self.start_diff)
        return {"difference": self.format_difference(difference)}

    def format_difference(difference: int) -> float:
        return round(difference / 6000, 2)

    def get_difficulty(self, session: Session) -> int:
        """
        Args:
            session: the session
            multiplier: float with three different possible values:
                1.5 multiplier for difference *increase*
                1 if difference should stay the same
                0.5 for difference *decrease*

        Returns:
            an integer indicating the inter-onset-interval in milliseconds
        """
        difficulty = session.json_data.get("difficulty")
        if not difficulty:
            difficulty = self.start_diff
            session.save_json_data({"difficulty": self.start_diff})
            return difficulty
        if not session.json_data.get("practice_done"):
            return difficulty
        last_result = session.last_result()
        if not last_result:
            return difficulty
        multiplier = last_result.json_data.get("multiplier", 1.0)
        current_difficulty = difficulty * multiplier
        session.save_json_data({"difficulty": current_difficulty})
        # return rounded difficulty
        # this uses the decimal module, since round() does not work entirely as expected
        return int(Decimal(str(current_difficulty)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

    def practice_successful(self, session: Session) -> bool:
        previous_results = session.last_n_results(n_results=2)
        return all(r.score > 0 for r in previous_results)

    def get_condition(self, session: Session) -> str:
        if not session.json_data.get("practice_done"):
            return super().get_condition(session)
        else:
            return self.get_trial_condition(session)

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
