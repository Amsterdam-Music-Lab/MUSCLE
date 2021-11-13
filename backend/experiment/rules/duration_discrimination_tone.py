from django.utils.translation import gettext as _

from .duration_discrimination import DurationDiscrimination

class DurationDiscriminationTone(DurationDiscrimination):
    ID = 'DURATION_DISCRIMINATION_TONE'
    condition = _('tone')

    @classmethod
    def get_score_message(cls, milliseconds):
        return _('Well done! You managed to hear the difference between tones that \
                differed only {} milliseconds in length. Humans are really good at \
                hearing these small differences in durations, which is very handy \
                if we want to be able to process rhythm in music.').format(milliseconds)
    
    @classmethod
    def get_response_explainer(cls, correct, correct_response, button_label=_('Next fragment')):
        preposition = _('than') if correct_response=='LONGER' else _('as')
        if correct:
            instruction = _(
                'The second tone was %(correct_response)s %(preposition)s the first tone. Your answer was correct.') % {'correct_response': correct_response, 'preposition': preposition}
        else:
            instruction = _(
                'The second tone was %(correct_response)s %(preposition)s the first tone. Your answer was incorrect.') % {'correct_response': correct_response, 'preposition': preposition}
        return Explainer.action(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )
    
    @classmethod
    def get_question_text(cls):
        return _("Is the second tone LONGER than the first tone or EQUALLY LONG?")

    @classmethod
    def get_task_explanation(cls):
        return _("It's your job to decide if the second tone is LONGER than the first tone, or EQUALLY LONG.")