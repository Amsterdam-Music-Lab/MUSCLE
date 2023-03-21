from django.utils.translation import gettext_lazy as _

from .styles import STYLE_NEUTRAL

class Question(object):
    ''' Question is part of a form.
    - key: description of question in results table
    - view: which widget the question should use in the frontend
    - explainer: optional instructions for this specific question
    - question: the question text
    - scoring_rule: optionally, specify a scoring rule which should be applied
    - is_skippable: whether the question can be skipped
    - submits: whether entering a value for the question submits the form
    - style: one (string) or multiple (dict) class names to apply for styling the frontend component
    '''

    def __init__(
        self,
        key,
        result_id=None,
        view='STRING',
        explainer='',
        question='',
        is_skippable=False,
        submits=False,
        style=STYLE_NEUTRAL
        ):

        self.key = key
        self.view = view
        self.explainer = explainer
        self.question = question
        self.result_id = result_id
        self.is_skippable = is_skippable
        self.submits = submits
        self.style = style

    def action(self):
        return self.__dict__


class BooleanQuestion(Question):
    def __init__(self, choices=None, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices or {
            'yes': _('YES'),
            'no': _('NO')
        }
        self.view = 'BUTTON_ARRAY'


class ChoiceQuestion(Question):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices


class DropdownQuestion(Question):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.view = 'DROPDOWN'


class AutoCompleteQuestion(Question):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.view = 'AUTOCOMPLETE'


class RadiosQuestion(Question):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.view = 'RADIOS'


class ButtonArrayQuestion(Question):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.view = 'BUTTON_ARRAY'


class RangeQuestion(Question):
    def __init__(self, min_value, max_value, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value


class LikertQuestion(Question):
    def __init__(self, scale_steps=7, explainer=_("How much do you agree or disagree?"), likert_view='TEXT_RANGE', choices = {}, **kwargs):
        super().__init__(**kwargs)
        self.view = likert_view
        self.scoring_rule = 'LIKERT'
        self.scale_steps = scale_steps
        self.explainer = explainer

        if choices:
            self.choices = choices
            self.scale_steps = len(self.choices)
        else:
            if scale_steps == 7:
                self.choices = {
                    1: _("Completely Disagree"),
                    2: _("Strongly Disagree"),
                    3: _("Disagree"),
                    4: _("Neither Agree nor Disagree"),  # Undecided
                    5: _("Agree"),
                    6: _("Strongly Agree"),
                    7: _("Completely Agree"),
                }
            elif scale_steps == 5:
                self.choices = {
                    1: _("Strongly Disagree"),
                    2: _("Disagree"),
                    3: _("Neither Agree nor Disagree"),  # Undecided
                    4: _("Agree"),
                    5: _("Strongly Agree"),
                }

class LikertQuestionIcon(Question):
    def __init__(self, scale_steps=7, likert_view='ICON_RANGE', **kwargs):
        super().__init__(**kwargs)
        self.view = likert_view
        if scale_steps == 7:
            self.choices = {
                1: 'fa-face-angry',
                2: 'fa-face-frown-open',
                3: 'fa-face-frown',
                4: 'fa-face-meh',  # Undecided
                5: 'fa-face-smile',
                6: 'fa-face-grin',
                7: 'fa-face-grin-hearts',
            }
            self.config = {'icons':True, 'colors': ['#0CC7F1', '#42b5ff',  '#8b9bfa', '#ab86f1', '#bb7ae9', '#c863e8', '#d843e2']}
        elif scale_steps == 5:
            self.choices = {
                1: _("Strongly Disagree"),
                2: _("Disagree"),
                3: _("Neither Agree nor Disagree"),  # Undecided
                4: _("Agree"),
                5: _("Strongly Agree"),
            }

class Form(object):
    ''' Form is a view which brings together an array of questions with submit and optional skip button
    - form: array of questions
    - button_label: label of submit button
    - skip_label: label of skip button
    - is_skippable: can this question form be skipped
    '''

    def __init__(self, form, submit_label=_('Continue'), skip_label=_('Skip'), is_skippable=False):
        self.form = form
        self.submit_label = submit_label
        self.skip_label = skip_label
        self.is_skippable = is_skippable

    def action(self):
        serialized_form = [question.action() for question in self.form]
        return {
            'form': serialized_form,
            'submit_label': self.submit_label,
            'skip_label': self.skip_label,
            'is_skippable': self.is_skippable,
        }
