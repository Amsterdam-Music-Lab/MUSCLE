from django.utils.translation import gettext_lazy as _

from experiment.actions.button import Button
from experiment.actions.explainer import Explainer, Step
from question.banks import get_question_bank
from session.models import Session
from .base import BaseRules


class RhythmBatteryFinal(BaseRules):
    """ an experiment view that implements the GoldMSI questionnaire """
    ID = 'RHYTHM_BATTERY_FINAL'
    debrief_form = 'final/debrief_rhythm_unpaid.html'
    show_participant_final = False

    def __init__(self):
        self.question_lists = [
            {
                "name": "MSI_F3_MUSICAL_TRAINING",
                "question_identifiers": get_question_bank('MSI_F3_MUSICAL_TRAINING'),
                "randomize": True,
            },
            {
                "name": "Demographics",
                "question_identifiers": [
                    'dgf_gender_identity',
                    'dgf_age',
                    'dgf_education_gold_msi',
                    'dgf_highest_qualification_expectation',
                    'dgf_country_of_residence',
                    'dgf_country_of_origin',
                ],
                "randomize": False,
            },
        ]

    def get_intro_explainer(self):
        return Explainer(
            _(
                'Finally, we would like to ask you to answer some questions about your musical and demographic background.'
            ),
            steps=[
                Step(
                    _(
                        'After these questions, the experiment will proceed to the final screen.'
                    )
                )
            ],
            button=Button(_('Ok')),
        )

    def next_round(self, session: Session):
        questions = self.get_profile_question_trials(session, None)
        if questions:
            return [self.get_intro_explainer(), *questions]
        else:
            return self.get_final_view(session)

    def feedback_info(self):
        info = super().feedback_info()
        return info
