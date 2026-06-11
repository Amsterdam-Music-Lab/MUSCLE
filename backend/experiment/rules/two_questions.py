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
from question.models import Question
from result.utils import prepare_result
from session.models import Session

logger = logging.getLogger(__name__)


class TwoQuestions(BaseRules):
    """ Simple experiment presenting an audio file with Likert scale"""
    ID = "TWO_QUESTIONS"

    def get_intro_explainer(self, session: Session):
        """Explain the game"""
        explainer_identifier = session.block.rules_config.get(
            "intro_explainer", "explainer_fallback_dummy"
        )
        try:
            Explainer.objects.get(identifier=explainer_identifier).convert_to_action()
        except:
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
            return [
                self.get_intro_explainer(session),
                self.get_trial(session, total_rounds),
            ]
        elif round_number == total_rounds:
            session.finish()
            return [
                Final(
                    session,
                    title=_("End of this part"),
                    final_text=_("Thank you for your responses!"),
                )
            ]
        else:
            return [self.get_trial(session, total_rounds)]

    def get_trial(self, session, total_rounds):
        question1_identifier = session.block.rules_config.get(
            "question1_identifier", "question1_fallback_dummy"
        )
        played_sections = session.result_set.filter(
            question_identifier=question1_identifier
        ).values_list('section__id', flat=True)
        question2_identifier = session.block.rules_config.get(
            "question2_identifier", "question2_fallback_dummy"
        )
        section = session.playlist.get_section(exclude={'pk__in': played_sections})
        playback = Autoplay(sections=[PlaybackSection(section)], show_animation=False)
        try:
            question1 = Question.objects.get(
                identifier=question1_identifier
            ).convert_to_action()
        except:
            question1 = self.get_fallback_question(question1_identifier)
        question1.result_id = prepare_result(
            question1_identifier,
            session,
            section=section,
            scoring_rule=(
                getattr(question1, 'scoring_rule')
                if hasattr(question1, 'scoring_rule')
                else "LIKERT"
            ),
        )
        try:
            question2 = Question.objects.get(
                identifier=question2_identifier
            ).convert_to_action()
        except:
            question2 = self.get_fallback_question(question2_identifier)
        question2.result_id = prepare_result(
            question2_identifier,
            session,
            section=section,
            scoring_rule=(
                getattr(question2, 'scoring_rule')
                if hasattr(question2, 'scoring_rule')
                else "LIKERT"
            ),
        )
        form = Form(form=[question1, question2])
        return Trial(
            playback=playback,
            feedback_form=form,
            title=_("Round %(round_number)d of %(total_rounds)d")
            % {'round_number': len(played_sections), 'total_rounds': total_rounds},
            response_time=section.duration,
            listen_first=True,
        )

    def get_fallback_question(self, question_identifier: str) -> TextRangeQuestion:
        return TextRangeQuestion(
            identifier=question_identifier,
            text=_("Rate from lowest to highest"),
            choices=[
                {"value": 1, "label": _("Lowest")},
                {"value": 2, "label": _("Low")},
                {"value": 3, "label": _("Medium")},
                {"value": 4, "label": _("High")},
                {"value": 5, "label": _("Highest")},
            ],
        )
