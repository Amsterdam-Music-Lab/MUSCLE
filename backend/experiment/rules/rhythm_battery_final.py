from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.actions import Explainer, Final, Step
from experiment.questions.goldsmiths import MSI_F3_MUSICAL_TRAINING
from experiment.questions.demographics import EXTRA_DEMOGRAPHICS
from experiment.questions.utils import question_by_key

from .base import Base


class RhythmBatteryFinal(Base):
    """ an experiment view that implements the GoldMSI questionnaire """
    ID = 'RHYTHM_BATTERY_FINAL'
    debrief_form = 'final/debrief_rhythm_unpaid.html'
    show_participant_final = False

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
        explainer = Explainer(
            _('Finally, we would like to ask you to answer some questions about your musical and demographic background.'),
            steps=[
                Step(
                    _('After these questions, the experiment will proceed to the final screen.'))
            ],
            button_label=_('Ok')
        )
        return [explainer]

    def next_round(self, session):
        questions = self.get_questionnaire(session)
        if questions:
            return questions
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
