import math
import random
from typing import Tuple, Union

from django.utils.translation import gettext_lazy as _

from experiment.actions.button import Button
from experiment.actions.explainer import Explainer, Step
from experiment.actions.form import Form
from experiment.actions.playback import Autoplay, PlaybackSection
from experiment.actions.question import ButtonArrayQuestion
from experiment.actions.trial import Trial
from result.utils import prepare_result
from section.models import Section
from session.models import Session


class PracticeMixin(object):
    """PracticeMixin can be used to present a trial a given number of times.
    After these practice trials, it tests whether the partcipant performed well enough to proceed.

    Extend this class in your ruleset if you need a practice run for your participants.

    Note that you could use this class to
        - create rules for a self-contained block with only the practice run, and define the experiment proper in another rules file;
        - create rules which include the experiment proper after the practice phase.

    This practice class is now written towards 2 alternative forced choice rulesets, but may be extended in the future.

    Arguments:
        task_description (str): will appear in the title of the experiment
        first_condition (str): the first condition that trials may have (e.g., lower pitch)
        first_condition_i18n (str): the way the condition will appear to participants, can be translated if you use _() around the string
        second_condition (str): the second condition that trials may have (e.g., higher pitch)
        second_condition_i18n (str): the way the condition will appear to participants, can be translated if you use _() around the string
        n_practice_rounds (int): adjust to the number of practice rounds that should be presented
        n_practice_rounds_second_condition (int): how often the second condition appears in the practice rounds, e.g., one "catch" trial, or half the practice trials
        n_correct (int): how many answers of the participant need to be correct to proceed


    Example:
        This is an example of a rules file which would only present the practice run to the participant:
        ```python
        class MyPracticeRun(BaseRules, PracticeMixin):
            task_description = ""
            first_condition = 'lower'
            first_condition_i18n = _("LOWER")
            second_condition = 'higher'
            second_condition_i18n = _("HIGHER")
            n_practice_rounds = 10
            n_practice_rounds_second_condition = 5
            n_correct = 3

            def next_round(self, session):
                return self.next_practice_round(session)
        ```
        For a full-blown example, refer to the `duration_discrimination.py` rules file. This implements the experiment proper after the practice run.
    """

    task_description = "Pitch discrimination"
    first_condition = 'lower'
    first_condition_i18n = _("LOWER")
    second_condition = 'higher'
    second_condition_i18n = _("HIGHER")
    n_practice_rounds = 4
    n_practice_rounds_second_condition = 1  # how many trials have second condition
    n_correct = 1 # how many trials need to be answered correctly to proceed

    def next_practice_round(self, session: Session) -> list[Union[Trial, Explainer]]:
        """This method implements the logic for presenting explainers, practice rounds,
        and checking after the practice rounds if the participant was successful.

        - if so: proceed to the next stage of the experiment. `session.json_data` will have set `{'practice_done': True}`, which you can check for in your `next_round` logic.

        - if not: delete all results so far, and restart the practice.

        You can call this method from your ruleset's `next_round` function.

        Arguments:
            session: the Session object, as also supplied to `next_round`

        Returns:
            list of Trial and/or Explainer objects
        """
        round_number = session.get_rounds_passed()
        if round_number == 0:
            return [
                self.get_intro_explainer(),
                self.get_practice_explainer(),
                self.get_next_trial(session),
            ]
        if round_number % self.n_practice_rounds == 0:
            if self.practice_successful(session):
                self.finalize_practice(session)
                return [
                    self.get_feedback_explainer(session),
                    self.get_continuation_explainer(),
                ]
            else:
                # generate feedback, then delete all results so far and start over
                feedback = self.get_feedback_explainer(session)
                session.result_set.all().delete()
                return [
                    feedback,
                    self.get_restart_explainer(),
                    self.get_intro_explainer(),
                    self.get_practice_explainer(),
                    self.get_next_trial(session),
                ]
        else:
            return [
                self.get_feedback_explainer(session),
                self.get_next_trial(session),
            ]

    def finalize_practice(self, session: Session):
        """Finalize practice: set `{"practice_done": True}` in `session.json_data`

        Arguments:
            session: the Session object, as supplied to the `next_round` method
        """
        session.save_json_data({"practice_done": True})

    def get_intro_explainer(self) -> Explainer:
        """Override this method to explain the procedure of the current block to your participants.

        Returns:
            Explainer object
        """
        return Explainer(
            instruction=_("In this test you will hear two tones"),
            steps=[
                Step(
                    _(
                        "It's your job to decide if the second tone is %(first_condition)s or %(second_condition)s  than the second tone"
                    )
                    % {
                        "first_condition": self.first_condition_i18n,
                        "second_condition": self.second_condition_i18n,
                    }
                ),
                Step(
                    _(
                        "During the experiment it will become more difficult to hear the difference."
                    )
                ),
                Step(
                    _(
                        "Try to answer as accurately as possible, even if you're uncertain."
                    )
                ),
                Step(
                    _(
                        "This test will take around 4 minutes to complete. Try to stay focused for the entire test!"
                    )
                ),
            ],
            button=Button("Ok"),
            step_numbers=True,
        )

    def get_practice_explainer(self) -> Explainer:
        """Override this method if you want to give extra information about the practice itself.

        Returns:
            Explainer object
        """
        return Explainer(
            instruction=_("We will now practice first."),
            steps=[
                Step(
                    description=_(
                        "First you will hear %(n_practice_rounds)d practice trials."
                    )
                    % {"n_practice_rounds": self.n_practice_rounds}
                ),
            ],
            button=Button(_("Begin experiment")),
        )

    def get_restart_explainer(self) -> Explainer:
        """Override this method if you want to adjust the feedback to why participants need to practice again.

        Returns:
            Explainer object
        """
        return Explainer(
            instruction=_(
                "You have answered %(n_correct)d or more practice trials incorrectly."
            )
            % {"n_correct": self.n_correct},
            steps=[
                Step(_("We will therefore practice again.")),
                Step(_("But first, you can read the instructions again.")),
            ],
            button=Button(_("Continue")),
        )

    def get_continuation_explainer(self) -> Explainer:
        """Override this explainer if you want to give extra information to the participant before the actual test phase starts.
        Returns:
            Explainer object
        """
        return Explainer(
            instruction=_('Now we will start the real experiment.'),
            steps=[
                Step(
                    _(
                        'Pay attention! During the experiment it will become more difficult to hear the difference between the tones.'
                    )
                ),
                Step(
                    _(
                        "Try to answer as accurately as possible, even if you're uncertain."
                    )
                ),
                Step(_("Remember that you don't move along or tap during the test.")),
            ],
            step_numbers=True,
            button=Button(_('Start')),
        )

    def get_feedback_explainer(self, session: Session) -> Explainer:
        """Override this explainer if you need to give different feedback to participants about whether or not they answered correctly.

        Returns:
            Explainer object
        """
        correct_response, is_correct = self.get_condition_and_correctness(session)
        if is_correct:
            instruction = _(
                "The second tone was %(correct_response)s than the first tone. Your answer was CORRECT."
            ) % {"correct_response": correct_response}
        else:
            instruction = _(
                "The second tone was %(correct_response)s than the first tone. Your answer was INCORRECT."
            ) % {"correct_response": correct_response}
        return Explainer(instruction=instruction, steps=[], button=Button(_('Ok')))

    def get_condition_and_correctness(self, session: Session) -> Tuple[str, bool]:
        """Checks whether the condition of the last Trial, and whether the response of the participant was correct.
        This method is called from `get_feedback_explainer`.

        Args:
            session: Session object, as supplied to the `next_round` method

        Returns:
            a tuple of the last trial's condition, and whether it was answered correctly
        """
        last_result = session.last_result()
        correct_response = (
            self.first_condition_i18n
            if last_result.expected_response == self.first_condition
            else self.second_condition_i18n
        )
        return (
            correct_response,
            last_result.expected_response == last_result.given_response,
        )

    def get_condition(self, session: Session) -> str:
        """Keep track of the conditions presented in the practice phase through the `session.json_data`.
        In the default implementation, it will generate `n_practice_rounds` conditions, with `n_second_condition` times the second condition,
        and `n_practice_rounds - n_second_condition` times the first condition, shuffle these randomly,
        and then present one condition each round.

        Override this method if you need a different setup.

        Arguments:
            session: the Session object, as supplied to the `next_round` method
        """
        conditions = session.json_data.get("conditions")
        if not conditions:
            conditions = [
                self.first_condition
            ] * self.n_practice_rounds_second_condition + [self.second_condition] * (
                self.n_practice_rounds - self.n_practice_rounds_second_condition
            )
            while conditions[-2] == conditions[-1]:
                # we want the conditions shuffled so that we don't get the same condition twice right away
                random.shuffle(conditions)
            session.save_json_data({'conditions': conditions})
        condition = conditions.pop()
        session.save_json_data({'conditions': conditions})
        session.save()
        return condition

    def get_next_trial(self, session: Session) -> Trial:
        """
        Provide the next trial action

        Args:
            session: the Session object, as supplied to the `next_round` function

        Returns:
            Trial object
        """
        round_number = session.get_rounds_passed()
        condition = self.get_condition(session)
        try:
            section = session.playlist.get_section(
                {"group": "practice", "tag": condition}
            )
        except Section.DoesNotExist:
            raise
        expected_response = condition
        total_rounds = self.n_practice_rounds * math.ceil(
            round_number / self.n_practice_rounds
        )
        key = self.task_description.replace(" ", "_") + "_practice"
        question = ButtonArrayQuestion(
            text=_(
                "Is the second tone %(first_condition)s or %(second_condition)s than the first tone?"
            )
            % {
                "first_condition": self.first_condition_i18n,
                "second_condition": self.second_condition_i18n,
            },
            key=key,
            choices={
                self.first_condition: self.first_condition_i18n,
                self.second_condition: self.second_condition_i18n,
            },
            result_id=prepare_result(
                key,
                session,
                section=section,
                expected_response=expected_response,
                scoring_rule="CORRECTNESS",
            ),
        )
        playback = Autoplay(sections=[PlaybackSection(section)])
        form = Form([question], submit_button=None)
        return Trial(
            playback=playback,
            feedback_form=form,
            title=_(
                "%(task_description)s: Practice round %(round_number)d of %(total_rounds)d"
                % {
                    "task_description": self.task_description,
                    "round_number": round_number + 1,
                    "total_rounds": total_rounds,
                }
            ),
            listen_first=True,
            response_time=section.duration + 0.1,
        )

    def practice_successful(self, session: Session) -> bool:
        """Checks if the practice is correct, i.e., that at the participant gave at least `n_correct` correct responses.

        Override this method if you need different logic.

        Arguments:
            session: the Session object, as supplied to the `next_round` method

        Returns:
            a boolean indicating whether or not the practice was successful
        """
        results = session.last_n_results(n_results=self.n_practice_rounds)
        correct = sum(result.score for result in results)
        return correct >= self.n_correct
