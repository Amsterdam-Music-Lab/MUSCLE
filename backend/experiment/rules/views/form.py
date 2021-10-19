from django.utils.translation import gettext_lazy as _
import json

class Question(object):
    ''' Question is part of a form.
    - key: description of question in results table
    - explainer: optional instructions for this specific question
    - question: the question text
    - result_pk: identifier of result object, created prior to sending next_round data to client
    - is_skippable: whether a value has to be set on the question before form can be submitted
    - submits: whether changing this form element can submit the form
    '''

    def __init__(self, key, view, result_id=None, explainer='', question='', is_skippable=False, submits=False):
        self.key = key
        self.view = view
        self.explainer = explainer,
        self.question = question,
        self.result_id = result_id
        self.is_skippable = is_skippable
        self.submits = submits
    
    def action(self):
        return self.__dict__


class ChoiceQuestion(Question):
    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices

class RangeQuestion(Question):
    def __init__(self, min_value, max_value, *args):
        super().__init__(*args)
        self.min_value = min_value
        selfmax_value = max_value

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
            'is_skippable': self.is_skippable
        }