from django.utils.translation import gettext_lazy as _

from experiment.actions import Trial, Consent, StartSession
from experiment.actions.form import Form
from experiment.util.goldsmiths import MSI_F3_MUSICAL_TRAINING
from experiment.util.questions import EXTRA_DEMOGRAPHICS, question_by_key
from experiment.util.actions import final_action_with_optional_button

from .base import Base


class GoldMSI(Base):
    """ an experiment view that implements the GoldMSI questionnaire """
    ID = 'GOLD_MSI'
    demographics = [
        question_by_key('dgf_gender_identity'),
        question_by_key('dgf_age', EXTRA_DEMOGRAPHICS),
        question_by_key('dgf_education', drop_choices=['isced-1']),
        question_by_key('dgf_highest_qualification_expectation',
                        EXTRA_DEMOGRAPHICS),
        question_by_key('dgf_country_of_residence'),
        question_by_key('dgf_country_of_origin'),
    ]
    questions = MSI_F3_MUSICAL_TRAINING + demographics

    @classmethod
    def first_round(cls, experiment, participant):
        consent = Consent.action()
        start_session = StartSession.action()
        return [
            consent,
            start_session
        ]

    @classmethod
    def next_round(cls, session, request_session=None):
        round_number = session.total_questions()
        if round_number == len(cls.questions):
            return final_action_with_optional_button(session, '', request_session)
        question = cls.questions[round_number]
        question.prepare_result(session, scoring_rule=MSI_SCORING_RULES.get(question.key, ''))
        feedback_form = Form([
            question,
        ], is_profile=True)
        view = Trial(None, feedback_form)
        return view.action()
