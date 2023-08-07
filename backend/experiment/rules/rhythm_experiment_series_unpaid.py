from django.utils.translation import gettext as _

from experiment.actions import Explainer, Step

from . import RhythmExperimentSeries

class RhythmExperimentSeriesUnpaid(RhythmExperimentSeries):
    ID = 'RHYTHM_SERIES_UNPAID'
    consent_form = 'consent/consent_rhythm_unpaid.html'
    debrief_form = 'final/debrief_rhythm_unpaid.html'
    show_participant_final = False

    @classmethod
    def intro_explainer(cls):
        return Explainer(
            instruction=_("You are about to take part in an experiment about rhythm perception."),
            steps=[
                Step(_(
                        "We want to find out what the best way is to test whether someone has a good sense of rhythm!"),
                ),
                Step(_(
                        "You will be doing many little tasks that have something to do with rhythm."),
                ),
                Step(_(
                        "You will get a short explanation and a practice trial for each little task."),
                ),
                Step(_(
                        "We are very grateful for your participation!"),
                )
            ],
            button_label=_("Continue")
        )
