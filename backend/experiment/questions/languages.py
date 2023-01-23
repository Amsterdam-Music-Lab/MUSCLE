from django.utils.translation import gettext_lazy as _

from experiment.actions import Question

LANGUAGE = [
    Question.radios(
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
    Question.string(
        key='lang_mother',
        question=_('What is your mother tongue?')),
    Question.string(
        key='lang_second',
        # explainer='You can skip this question',
        question=_('What is your second language, if applicable?'), is_skippable=True),
    Question.string(
        key='lang_third',
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
        return Question.action(
            question={
                'view': 'RADIOS',
                'key': key,
                'question': question,
                'explainer': '',
                'choices': choices,
                'is_skippable': False,
            },
            title=_('Exposure to {}').format(self.language)
        )
