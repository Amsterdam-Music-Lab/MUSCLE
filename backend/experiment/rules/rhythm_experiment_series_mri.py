from django.utils.translation import gettext as _

from . import RhythmExperimentSeries
from experiment.actions import Explainer, Step


class RhythmExperimentSeriesMRI(RhythmExperimentSeries):
    ID = 'RHYTHM_SERIES_MRI'
    consent_form = 'consent/consent_MRI.html'
    debrief_form = 'final/debrief_MRI.html'
    show_participant_final = False

    def intro_explainer(self):
        return Explainer(
            instruction=_("You are about to take part in an experiment about rhythm perception."),
            steps=[
                Step(_(
                        "We want to find out which brain areas are involved in our sense of rhythm!"),
                ),
                Step(_(
                        "You will be doing many little tasks that have something to do with rhythm."),
                ),
                Step(_(
                        "You will get a short explanation and a practice trial for each little task."),
                ),
                Step(_(
                        "You will receive 15 euros as compensation for your participation. You will get instructions for how to get paid at the end of the experiment."),
                )
            ],
            button_label=_("Continue")
        )