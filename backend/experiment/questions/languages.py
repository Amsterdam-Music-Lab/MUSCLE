from django.utils.translation import gettext_lazy as _

from experiment.actions.form import Question, RadiosQuestion, TextQuestion

LANGUAGE = [
    RadiosQuestion(
        key='lang_experience',
        question=_("Please rate your previous experience:"),
        choices={
            'fluent': _("fluent"),
            'intm': _("intermediate"),
            'beginner': _("beginner"),
            'some_exp': _("some exposure"),
            'no_exp': _("no exposure")
        }
    ),
    TextQuestion(
        key='lang_mother',
        view='STRING',
        question=_('What is your mother tongue?')),
    TextQuestion(
        key='lang_second',
        view='STRING',
        # explainer='You can skip this question',
        question=_('What is your second language, if applicable?'), is_skippable=True),
    TextQuestion(
        key='lang_third',
        view='STRING',
        # explainer='You can skip this question',
        question=_('What is your third language, if applicable?'), is_skippable=True)
]


class LanguageQuestion(Question):
    def __init__(self, language):
        self.language = language

    def exposure_question(self):
        key = 'lang_exposure_{}'.format(self.language)
        question = _('Please rate your previous experience with {}').format(
            self.language)
        choices = {
            'fluent': _("fluent"),
            'intm': _("intermediate"),
            'beginner': _("beginner"),
            'some_exp': _("some exposure"),
            'no_exp': _("no exposure")
        }
        return RadiosQuestion(
            key=key,
            question=question,
            choices=choices
        )
