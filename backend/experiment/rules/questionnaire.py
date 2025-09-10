from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from session.models import Session
from experiment.actions import Explainer, Redirect

class Questionnaire(BaseRules):
    """ a rules file which does not do anything but show a questionnaire """
    ID = 'QUESTIONNAIRE'
    debrief_form = 'final/debrief_rhythm_unpaid.html'
    show_participant_final = False

    def next_round(self, session: Session):
        actions = []

        questions = self.get_open_questions(session)
        if questions:
            intro_questions = Explainer(
                instruction=_(
                    "Before starting the game, we would like to ask you {} demographic questions."
                ).format(len(questions)),
                steps=[],
            )
            actions.append(intro_questions)
            actions.extend(questions)
            return actions

        session.finish()
        session.save()
        return Redirect(settings.RELOAD_PARTICIPANT_TARGET)
