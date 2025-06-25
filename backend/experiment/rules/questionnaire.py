from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from session.models import Session
from experiment.actions import Explainer, Redirect
from random import choice


class Questionnaire(BaseRules):
    """a rules file which does not do anything but show a questionnaire"""

    ID = "QUESTIONNAIRE"
    debrief_form = "final/debrief_rhythm_unpaid.html"
    show_participant_final = False

    def next_round(self, session: Session):
        actions = []

        questions = self.get_open_questions(session)
        if questions:
            intro_questions = Explainer(
                instruction=_(
                    "Before starting the game, we would like to ask you %i demographic questions."
                    % (len(questions))
                ),
                steps=[],
            )
            actions.append(intro_questions)
            actions.extend(questions)

        # Temporary hack: just redirect to a random block.
        blocks = session.block.phase.experiment.associated_blocks()
        other_blocks = []
        for block in blocks:
            rules = block.get_rules()
            if rules.__class__ != self.__class__:
                other_blocks += [block]
        next_block = choice(other_blocks)
        experiment_url = self.get_experiment_url(session)
        actions.append(
            Redirect(f"{experiment_url}/block/{next_block.slug}")
            # Redirect(settings.RELOAD_PARTICIPANT_TARGET)
        )
        return actions
