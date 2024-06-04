import logging
from django.template.loader import render_to_string
from os.path import join
from .toontjehoger_1_mozart import toontjehoger_ranks
from .toontjehoger_6_relative import ToontjeHoger6Relative
from experiment.actions import Trial, Explainer, Step, Score, Final, Playlist, Info
from experiment.actions.form import ChoiceQuestion, Form
from experiment.actions.playback import Multiplayer
from experiment.actions.styles import STYLE_BOOLEAN

from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHogerKids6Relative(ToontjeHoger6Relative):
    ID = 'TOONTJE_HOGER_KIDS_6_RELATIVE'

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Relatief Gehoor",
            steps=[
                Step("In deze mini-game kun je jouw relatief gehoor testen!"),
                # Empty step adds some spacing between steps to improve readability
                Step(""),
                Step(
                    "Je hoort steeds twee melodieën, de een wat hoger dan de andere.", number=1),
                Step("Luister goed, want je kunt ze maar één keer afspelen!", number=2),
                Step("Aan jou de taak om te luisteren of deze melodieën hetzelfde zijn, ongeacht de toonhoogte!", number=3),
            ],
            button_label="Start"
        )

        return [
            explainer,
        ]

    def get_score(self, session):
        # Feedback
        last_result = session.last_result()

        if not last_result:
            logger.error("No last result")
            feedback = "Er is een fout opgetreden"
        else:
            if last_result.score == self.SCORE_CORRECT:
                feedback = "Dat klopt! De melodieën zijn inderdaad verschillend."
            else:
                feedback = "Helaas! De melodieën zijn toch echt verschillend."

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback)
        return [score]

    def get_final_round(self, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session)

        # Final
        final_text = "Goed gedaan!" if session.final_score >= 2 * \
            self.SCORE_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment6.html'))
        info = Info(
            body=body,
            heading="Relatief gehoor",
            button_label="Terug naar ToontjeHoger",
            button_link="/toontjehoger"
        )

        return [*score, final, info]
