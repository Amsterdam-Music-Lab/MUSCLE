from django.utils.translation import gettext_lazy as _

from .views import Explainer
from .duration_discrimination import DurationDiscrimination

class DurationDiscriminationTone(DurationDiscrimination):
    ID = 'DURATION_DISCRIMINATION_TONE'
    condition = _('tone')

    @classmethod
    def get_score_message(cls, milliseconds):
        return _('Well done! You managed to hear the difference between tones that \
                differed only {} milliseconds in length.\n\nHumans are really good at \
                hearing these small differences in durations, which is very handy \
                if we want to be able to process rhythm in music.').format(milliseconds)
    
    @classmethod
    def get_response_explainer(cls, correct, correct_response, button_label=_('Next fragment')):
        preposition = _('than') if correct_response=='LONGER' else _('as')
        correct_response = _('LONGER') if correct_response=='LONGER' else _('EQUAL')
        if correct:
            instruction = _(
                'The second tone was %(correct_response)s %(preposition)s the first tone. Your answer was CORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        else:
            instruction = _(
                'The second tone was %(correct_response)s %(preposition)s the first tone. Your answer was INCORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        return Explainer.action(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )
    
    @classmethod
    def get_question_text(cls):
        return _("Is the second tone EQUALLY LONG as the first tone or LONGER?")

    @classmethod
    def get_task_explanation(cls):
        return _("It's your job to decide if the second tone is EQUALLY LONG as the first tone, or LONGER.")