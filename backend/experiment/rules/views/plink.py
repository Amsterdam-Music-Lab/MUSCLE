from django.utils.translation import gettext_lazy as _


class Plink(object):  # pylint: disable=too-few-public-methods
    """
    A custom view that handles a Plink question
    Relates to client component: Plink.js
    This question type is related to ToontjeHoger experiment 3
    """

    ID = 'PLINK'

    def __init__(self, section, main_question, choices, submit_label, dont_know_label, extra_questions=[], title='', result_id=''):
        '''
        - section: A section
        - main_question: Main question
        - choices: Question choices
        - dont_know_label: Don't know button label
        - submit_label: Submit button labvel
        - extra_questions: A list of additional questions
        - title: Page title
        '''
        self.section = section.simple_object()
        self.title = title
        self.main_question = main_question
        self.choices = choices
        self.submit_label = submit_label
        self.dont_know_label = dont_know_label
        self.extra_questions = extra_questions
        self.result_id = result_id

    def action(self):
        """
        Serialize data for experiment action
        """
        # Create action
        action = {
            'view': Plink.ID,
            'title': self.title,
            'resultId': self.result_id,
            'section': self.section,
            'mainQuestion': self.main_question,
            'choices': self.choices,
            'submitLabel': self.submit_label,
            'dontKnowLabel': self.dont_know_label,
            'extraQuestions': self.extra_questions,
        }

        return action
