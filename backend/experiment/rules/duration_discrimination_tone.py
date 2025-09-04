from django.utils.translation import gettext_lazy as _

from experiment.actions.explainer import Explainer
from experiment.actions.utils import render_feedback_trivia
from .duration_discrimination import DurationDiscrimination


class DurationDiscriminationTone(DurationDiscrimination):
    ID = 'DURATION_DISCRIMINATION_TONE'
    subtask = _("Tone")

    def get_final_text(self, difference):
        milliseconds = round(difference / 1000)
        feedback = _('Well done! You managed to hear the difference between tones that \
                differed only {} milliseconds in length.').format(milliseconds)
        trivia = _('Humans are really good at \
                hearing these small differences in durations, which is very handy \
                if we want to be able to process rhythm in music.')
        return render_feedback_trivia(feedback, trivia)

    def get_response_explainer(self, correct, correct_response, button_label=_('Next fragment')):
        preposition = _('than') if correct_response=='LONGER' else _('as')
        correct_response = _('LONGER') if correct_response=='LONGER' else _('EQUAL')
        if correct:
            instruction = _(
                'The second tone was %(correct_response)s %(preposition)s the first tone. Your answer was CORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        else:
            instruction = _(
                'The second tone was %(correct_response)s %(preposition)s the first tone. Your answer was INCORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        return Explainer(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )

    def get_question_text(self):
        return _("Is the second tone EQUALLY LONG as the first tone or LONGER?")

    def get_introduction(self):
        return _('In this test you will hear two tones on each trial.')

    def get_task_explanation(self):
        return _("It's your job to decide if the second tone is EQUALLY LONG as the first tone, or LONGER.")
