from django.utils.translation import gettext_lazy as _

from experiment.actions import Consent, FrontendStyle, EFrontendStyle
from question.goldsmiths import MSI_F3_MUSICAL_TRAINING
from question.demographics import EXTRA_DEMOGRAPHICS
from question.utils import question_by_key
from question.questions import QUESTION_GROUPS
from experiment.actions.utils import final_action_with_optional_button

from .base import Base


class GoldMSI(Base):
    """ an experiment view that implements the GoldMSI questionnaire """
    ID = 'GOLD_MSI'

    def __init__(self):
        self.question_series = [
            {
                "name": "MSI_F3_MUSICAL_TRAINING",
                "keys": QUESTION_GROUPS["MSI_F3_MUSICAL_TRAINING"],
                "randomize": False
            },
            {
                "name": "Demographics",
                "keys": [
                    'dgf_gender_identity',
                    'dgf_age',
                    'dgf_education_gold_msi',
                    'dgf_highest_qualification_expectation',
                    'dgf_country_of_residence',
                    'dgf_country_of_origin'
                ],
                "randomize": False
            },
        ]

    def first_round(self, experiment):
        # Consent with admin text or default text
        consent = Consent(experiment.consent)
        return [
            consent,
        ]

    def next_round(self, session):
        questions = self.get_questionnaire(session)
        if questions:
            return questions
        else:
            return final_action_with_optional_button(session)

    def feedback_info(self):
        info = super().feedback_info()
        return info
