from django.utils.translation import gettext_lazy as _

from experiment.actions.question import RadiosQuestion, TextQuestion

LANGUAGE = [
    RadiosQuestion(
        key='lang_experience',
        text=_("Please rate your previous experience:"),
        choices={
            'fluent': _("fluent"),
            'intm': _("intermediate"),
            'beginner': _("beginner"),
            'some_exp': _("some exposure"),
            'no_exp': _("no exposure"),
        },
    ),
    TextQuestion(key='lang_mother', text=_('What is your mother tongue?')),
    TextQuestion(
        key='lang_second',
        text=_('What is your second language, if applicable?'),
    ),
    TextQuestion(
        key='lang_third',
        text=_('What is your third language, if applicable?'),
    ),
]


def language_question(language):
    key = f"lang_exposure_{language}"
    text = _('Please rate your previous experience with {}').format(language)
    choices = {
        'fluent': _("fluent"),
        'intm': _("intermediate"),
        'beginner': _("beginner"),
        'some_exp': _("some exposure"),
        'no_exp': _("no exposure"),
    }
    return RadiosQuestion(key=key, text=text, choices=choices)


LANGUAGE_OTHER = [
    language_question(_('English')),
    language_question(_('Brazilian Portuguese')),
    language_question(_('Mandarin Chinese')),
]
