import logging
from django.utils.translation import gettext_lazy as _

from experiment.actions import Explainer, Step
from experiment.actions.utils import render_feedback_trivia
from .duration_discrimination import DurationDiscrimination

logger = logging.getLogger(__name__)


class Anisochrony(DurationDiscrimination):
    ID = 'ANISOCHRONY'
    start_diff = 180000
    practice_diff = 270000
    max_turnpoints = 8
    task_description = "Anisochrony"
    subtask = ""
    first_condition = "irregular"
    second_condition = "regular"
    first_condition_i18n = _("IRREGULAR")
    second_condition_i18n = _("REGULAR")
    section_count = 249

    def get_feedback_explainer(self, session):
        button_label = _("Next fragment")
        last_result = session.last_result()
        correct_response = (
            self.first_condition_i18n
            if last_result.expected_response == self.first_condition
            else self.second_condition_i18n
        )
        if last_result.given_response == last_result.expected_response:
            instruction = _(
                    'The tones were {}. Your answer was CORRECT.').format(correct_response)
        else:
            instruction = _(
                    'The tones were {}. Your answer was INCORRECT.').format(correct_response)
        return Explainer(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )

    def get_intro_explanainer(self):
        return Explainer(
            instruction=_(
                "In this test you will hear a series of tones for each trial."
            ),
            steps=[
                Step(
                    _("It's your job to decide if the tones sound REGULAR or IRREGULAR")
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
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(
                    _(
                        "This test will take around 4 minutes to complete. Try to stay focused for the entire test!"
                    )
                ),
            ],
            button_label=_("Ok"),
        )

    def get_final_text(self, difference):
        percentage = round(difference / 6000, 2)
        feedback = _(
            "Well done! You heard the difference when we shifted a tone by {} percent.").format(percentage)
        trivia = _("Many sounds in nature have regularity like a metronome. \
            Our brains use this to process rhythm even better!")
        return render_feedback_trivia(feedback, trivia)

    def get_difficulty(self, session):
        if not session.json_data.get("practice_done"):
            return self.practice_diff
        else:
            return super().get_difficulty(session)
