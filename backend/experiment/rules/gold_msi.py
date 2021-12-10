import logging

from django.utils.translation import gettext_lazy as _
from .views import CompositeView, Consent, Explainer, Final, Playlist, StartSession
from .views.form import Form
from .util.goldsmiths import MSI_F3_MUSICAL_TRAINING
from .util.actions import combine_actions

from .base import Base

class GoldMSI(Base):
    """ an experiment view that implements the GoldMSI questionnaire """
    ID = 'GOLD_MSI'
    questions = MSI_F3_MUSICAL_TRAINING
    
    @classmethod
    def first_round(cls, experiment):
        consent = Consent.action()
        start_session = StartSession.action()
        return combine_actions(
            consent,
            start_session
        )
    
    @classmethod
    def next_round(cls, session):
        round_number = session.total_questions()
        question = cls.questions[round_number]
        feedback_form = Form([
            question,
        ], is_profile=True)
        view = CompositeView(None, feedback_form.action())
        return view.action()
