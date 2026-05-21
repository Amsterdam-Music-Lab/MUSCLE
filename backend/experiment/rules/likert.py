import logging

from django.utils.translation import gettext_lazy as _

from action.models import Explainer
from experiment.actions.button import Button
from experiment.actions.explainer import Explainer as ExplainerAction, Step
from experiment.actions.final import Final
from experiment.actions.form import Form
from experiment.actions.playback import Autoplay, PlaybackSection
from experiment.actions.question import TextRangeQuestion
from experiment.actions.trial import Trial
from experiment.rules.base import BaseRules
from result.utils import prepare_result
from session.models import Session

logger = logging.getLogger(__name__)


class Likert(BaseRules):
    """ Simple experiment presenting an audio file with Likert scale"""
    ID = "LIKERT_EXPERIMENT"
    
    def get_intro_explainer(self, session: Session):
        """Explain the game"""
        explainer_identifier = session.block.rules_config.get('intro_explainer')
        if explainer_identifier:
            return Explainer.objects.get(identifier=explainer_identifier).convert_to_action()
        else:
            return ExplainerAction(
                instruction="Default question",
                steps=[
                    Step(
                        _(
                            "Step 1."
                        )
                    ),
                    Step(
                        _(
                            "Step 2."
                        )
                    ),
                ],
                step_numbers=True,
                button=Button(_("Let's go!")),
            )
    
    def next_round(self, session: Session):
        round_number = session.get_rounds_passed()
        total_rounds = session.playlist.section_set.count()
        if round_number == 0:
            return [self.get_intro_explainer(session)]
        elif round_number == total_rounds:
            return [
                Final(session, title=_("End of experiment"), final_text=_("Thank you for participating!"))
            ]
        else:
            return [self.get_trial(session, total_rounds)]

    def get_trial(self, session, total_rounds):
        question_key = 'likert'
        played_sections = session.result_set.filter(question_key=question_key).values_list('section__id', flat=True)
        section = session.playlist.get_section(exclude={'pk__in': played_sections})
        playback = Autoplay(sections=[PlaybackSection(section)])
        question = TextRangeQuestion(key=question_key, explainer=_("Rate from lowest to highest"), choices=[
            {"value": 1, "label": _("Lowest")},
            {"value": 2, "label": _("Low")},
            {"value": 3, "label": _("Medium")},
            {"value": 4, "label": _("High")},
            {"value": 5, "label": _("Highest")},
        ], result_id=prepare_result(question_key, session, scoring_rule="LIKERT", section=section))
        form = Form(form=[question])
        return Trial(
            playback=playback,
            feedback_form=form,
            title=_("Round %(round_number)d of %(total_rounds)d") % {'round_number': len(played_sections), 'total_rounds': total_rounds}
        )