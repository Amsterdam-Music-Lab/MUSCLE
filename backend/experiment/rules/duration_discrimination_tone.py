from django.utils.translation import gettext_lazy as _

from experiment.actions.button import Button
from experiment.actions.explainer import Explainer
from .duration_discrimination import DurationDiscrimination


class DurationDiscriminationTone(DurationDiscrimination):
    ID = 'DURATION_DISCRIMINATION_TONE'
    subtask = _("Tone")

    def format_difference(self, difference: int) -> float:
        return round(difference / 1000)

    def get_response_explainer(self, correct, correct_response, button_label=_('Next fragment')):
        preposition = _('than') if correct_response=='LONGER' else _('as')
        correct_response = _('LONGER') if correct_response=='LONGER' else _('EQUAL')
        if correct:
            instruction = _(
                'The second tone was %(correct_response)s %(preposition)s the first tone. Your answer was CORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        else:
            instruction = _(
                'The second tone was %(correct_response)s %(preposition)s the first tone. Your answer was INCORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        return Explainer(instruction=instruction, steps=[], button=Button(button_label))

    def get_question_text(self):
        return _("Is the second tone EQUALLY LONG as the first tone or LONGER?")

    def get_introduction(self):
        return _('In this test you will hear two tones on each trial.')

    def get_task_explanation(self):
        return _("It's your job to decide if the second tone is EQUALLY LONG as the first tone, or LONGER.")
