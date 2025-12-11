from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from experiment.actions.explainer import Explainer
from experiment.actions.redirect import Redirect
from session.models import Session

class Questionnaire(BaseRules):
    """ a rules file which does not do anything but show a questionnaire """
    ID = 'QUESTIONNAIRE'
    debrief_form = 'final/debrief_rhythm_unpaid.html'
    show_participant_final = False

    def next_round(self, session: Session):
        actions = []

        questions = self.get_profile_question_trials(session, None)
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
            return actions

        session.finish()
        session.save()
        return Redirect(session.block.phase.experiment.slug)
