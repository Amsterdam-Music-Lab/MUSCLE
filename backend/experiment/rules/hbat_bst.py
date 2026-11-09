from django.utils.translation import gettext_lazy as _

from experiment.actions.button import Button
from experiment.actions.explainer import Explainer, Step

from session.models import Session

from .h_bat import HBat


class BST(HBat):
    """ Rules for the BST experiment, which follow closely
    the HBAT rules. """
    ID = 'BST'
    first_condition = "in2"
    first_condition_i18n = _("DUPLE METER")
    second_condition = "in3"
    second_condition_i18n = _("TRIPLE METER")

    def get_intro_explainer(self):
        return Explainer(
            instruction=_(
                'In this test you will hear a number of rhythms which have a regular beat.'
            ),
            steps=[
                Step(
                    _(
                        "It's your job to decide if the rhythm has a DUPLE METER (a MARCH) or a TRIPLE METER (a WALTZ)."
                    )
                ),
                Step(
                    _(
                        "Every SECOND tone in a DUPLE meter (march) is louder and every THIRD tone in a TRIPLE meter (waltz) is louder."
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
                        "In this test, you can answer as soon as you feel you know the answer, but please wait until you are sure or the sound has stopped."
                    )
                ),
                Step(
                    _(
                        'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'
                    )
                ),
            ],
            button=Button('Ok'),
        )

    def get_trial_question(self):
        return _("Is the rhythm a DUPLE METER (MARCH) or a TRIPLE METER (WALTZ)?")

    def get_trial_title(self):
        return _("Meter detection")

    def get_feedback_explainer(self, session: Session):
        correct_response, is_correct = self.get_condition_and_correctness(session)
        if is_correct:
            instruction = _(
                "The rhythm was a %(correct_response)s. Your answer was CORRECT."
            ) % {"correct_response": correct_response}
        else:
            instruction = _(
                "The rhythm was a %(correct_response)s Your answer was INCORRECT."
            ) % {"correct_response": correct_response}
        return Explainer(
            instruction=instruction, steps=[], button=Button(_("Next fragment"))
        )

    def get_final_statistics(self, session: Session) -> dict:
        loudness_diff = int(self.get_average_difference(session, 6, self.start_diff))
        return {"loudness_diff": loudness_diff}
