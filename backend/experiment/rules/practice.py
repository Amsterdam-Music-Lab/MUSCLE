import math
import random
from typing import Tuple

from django.utils.translation import gettext_lazy as _

from experiment.actions import ChoiceQuestion, Form, Explainer, Score, Step, Trial
from experiment.actions.playback import Autoplay
from experiment.rules.base import Base
from result.utils import prepare_result
from section.models import Section
from session.models import Session

class Practice(Base):
    ''' Practice is a rules class which presents a trial n_practice_round times
    At the end of a set of practice rounds, it tests whether the partcipant performed well enough to proceed
    '''
    task_description = "Pitch discrimination"
    first_condition = 'lower'
    first_condition_i18n = _("LOWER")
    second_condition = 'higher'
    second_condition_i18n = _("HIGHER")
    n_practice_rounds = 4
    n_practice_rounds_second_condition = 1  # how many trials have first condition
    n_correct = 1 # how many trials need to be answered correctly to proceed

    def next_round(self, session: Session) -> list:
        return self.next_practice_round(session)

    def next_practice_round(self, session: Session) -> list:
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

    def finalize_practice(self, session):
        """Finalize practice"""
        session.save_json_data({"practice_done": True})

    def get_intro_explainer(self) -> Explainer:
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
            button_label="Ok",
            step_numbers=True,
        )

    def get_practice_explainer(self):
        return Explainer(
            instruction=_("We will now practice first."),
            steps=[
                Step(description=_("First you will hear 4 practice trials.")),
            ],
            button_label=_("Begin experiment"),
        )

    def get_restart_explainer(self) -> Explainer:
        return Explainer(
            instruction=_(
                "You have answered 1 or more practice trials incorrectly."),
            steps=[
                Step(_("We will therefore practice again.")),
                Step(_(
                    'But first, you can read the instructions again.')),
            ],
            button_label=_('Continue')
        )

    def get_continuation_explainer(self) -> Explainer:
        return Explainer(
            instruction=_(
                'Now we will start the real experiment.'),
            steps=[
                Step(_('Pay attention! During the experiment it will become more difficult to hear the difference between the tones.')),
                Step(_(
                        "Try to answer as accurately as possible, even if you're uncertain.")),
                Step(_(
                        "Remember that you don't move along or tap during the test.")),
            ],
            step_numbers=True,
            button_label=_('Start')
        )

    def get_feedback_explainer(self, session: Session) -> Explainer:
        correct_response, is_correct = self.get_condition_and_correctness(session)
        if is_correct:
            instruction = _(
                "The second tone was %(correct_response)s than the first tone. Your answer was CORRECT."
            ) % {"correct_response": correct_response}
        else:
            instruction = _(
                "The second tone was %(correct_response)s than the first tone. Your answer was INCORRECT."
            ) % {"correct_response": correct_response}
        return Explainer(
            instruction=instruction,
            steps=[],
            button_label=_('Ok')
        )

    def get_condition_and_correctness(self, session) -> Tuple[str, bool]:
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

    def get_condition(self, session) -> str:
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
            session: the session

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
        question = ChoiceQuestion(
            question=_(
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
            view="BUTTON_ARRAY",
            result_id=prepare_result(
                key,
                session,
                section=section,
                expected_response=expected_response,
                scoring_rule="CORRECTNESS",
            ),
            submits=True,
        )
        playback = Autoplay([section])
        form = Form([question])
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
            config={"listen_first": True, "response_time": section.duration + 0.1},
        )

    def practice_successful(self, session: Session) -> bool:
        results = session.last_n_results(n_results=self.n_practice_rounds)
        correct = sum(result.score for result in results)
        return correct >= self.n_correct
