from django.utils.translation import gettext_lazy as _

from experiment.actions import Consent, FrontendStyle, EFrontendStyle
from experiment.questions.goldsmiths import MSI_F3_MUSICAL_TRAINING
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.utils import question_by_key
from experiment.actions.utils import final_action_with_optional_button

from .base import Base


class GoldMSI(Base):
    """ an experiment view that implements the GoldMSI questionnaire """
    ID = 'GOLD_MSI'

    def __init__(self):
        demographics = [
            question_by_key('dgf_gender_identity'),
            question_by_key('dgf_age', EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_education', drop_choices=['isced-1']),
            question_by_key('dgf_highest_qualification_expectation',
                            EXTRA_DEMOGRAPHICS),
            question_by_key('dgf_country_of_residence'),
            question_by_key('dgf_country_of_origin'),
        ]
        self.questions = MSI_F3_MUSICAL_TRAINING + demographics

    def first_round(self, experiment):
        consent = Consent(
            style=FrontendStyle(
                EFrontendStyle.BOOLEAN,
                submit_button=FrontendStyle(
                    EFrontendStyle.SUCCESS
                )
            )
        )
        return [
            consent,
        ]

    def next_round(self, session, request_session=None):
        questions = self.get_questionnaire(session)
        if questions:
            return questions
        else:
            return final_action_with_optional_button(session, '', request_session)

    def feedback_info(self):
        info = super().feedback_info()
        return info
