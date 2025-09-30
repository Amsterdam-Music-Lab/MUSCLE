from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.actions.explainer import Explainer, Step
from experiment.actions.final import Final
from question.preset_catalogues import get_preset_catalogue
from .base import BaseRules


class RhythmBatteryFinal(BaseRules):
    """ an experiment view that implements the GoldMSI questionnaire """
    ID = 'RHYTHM_BATTERY_FINAL'
    debrief_form = 'final/debrief_rhythm_unpaid.html'
    show_participant_final = False

    def __init__(self):
        self.question_catalogues = [
            {
                "name": "MSI_F3_MUSICAL_TRAINING",
                "question_keys": get_preset_catalogue('MSI_F3_MUSICAL_TRAINING'),
                "randomize": True,
            },
            {
                "name": "Demographics",
                "question_keys": [
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
            _('Finally, we would like to ask you to answer some questions about your musical and demographic background.'),
            steps=[
                Step(
                    _('After these questions, the experiment will proceed to the final screen.'))
            ],
            button_label=_('Ok')
        )

    def next_round(self, session):
        questions = self.get_profile_question_trials(session, None)
        if questions:
            return [self.get_intro_explainer(), *questions]
        else:
            rendered = render_to_string(self.debrief_form)
            return Final(
                session,
                title=_("Thank you very much for participating!"),
                final_text=rendered,
                show_participant_link=self.show_participant_final,
                show_participant_id_only=self.show_participant_final,
            )

    def feedback_info(self):
        info = super().feedback_info()
        return info
