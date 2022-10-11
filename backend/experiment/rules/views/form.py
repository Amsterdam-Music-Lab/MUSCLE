import json

from django.utils.translation import gettext_lazy as _


class Question(object):
    ''' Question is part of a form.
    - key: description of question in results table
    - explainer: optional instructions for this specific question
    - question: the question text
    - result_pk: identifier of result object, created prior to sending next_round data to client
    - form_config: dictionary to set the following:
        - is_skippable: whether a value has to be set on the question before form can be submitted
        - submits: whether changing this form element can submit the form
        - show_labels: whether the labels of the answers should be shown
    '''

    def __init__(self, key, view='STRING', result_id=None, scoring_rule='NONE', explainer='', question='', is_skippable=False, submits=False):
        self.key = key
        self.view = view
        self.explainer = explainer
        self.question = question,
        self.result_id = result_id
        self.is_skippable = is_skippable
        self.submits = submits
        self.scoring_rule = scoring_rule

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
    def __init__(self, scale_steps=7, explainer=_("How much do you agree or disagree?"), likert_view='TEXT_RANGE', **kwargs):
        super().__init__(**kwargs)
        self.view = likert_view
        self.scoring_rule = 'LIKERT'
        self.scale_steps = scale_steps
        self.explainer = explainer
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

class Form(object):
    ''' Form is a view which brings together an array of questions with submit and optional skip button
    - form: array of questions
    - button_label: label of submit button
    - skip_label: label of skip button
    - is_skippable: can this question form be skipped
    - is_profile: should the answers be saved to the user profile
    '''

    def __init__(self, form, submit_label=_('Continue'), skip_label=_('Skip'), is_skippable=False, is_profile=False):
        self.form = form
        self.submit_label = submit_label
        self.skip_label = skip_label
        self.is_skippable = is_skippable
        self.is_profile = is_profile

    def action(self):
        serialized_form = [question.action() for question in self.form]
        return {
            'form': serialized_form,
            'submit_label': self.submit_label,
            'skip_label': self.skip_label,
            'is_skippable': self.is_skippable,
            'is_profile': self.is_profile,
        }
