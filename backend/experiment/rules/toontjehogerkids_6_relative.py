import logging
from django.template.loader import render_to_string
from os.path import join
from .toontjehoger_1_mozart import toontjehoger_ranks
from .toontjehoger_6_relative import ToontjeHoger6Relative
from experiment.actions import Explainer, Step, Score, Final, Info
from experiment.actions.utils import get_current_collection_url

logger = logging.getLogger(__name__)


class ToontjeHogerKids6Relative(ToontjeHoger6Relative):
    ID = 'TOONTJE_HOGER_KIDS_6_RELATIVE'

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Relatief Gehoor",
            steps=[
                Step("In dit testje kun je jouw relatief gehoor testen!"),
                # Empty step adds some spacing between steps to improve readability
                Step(""),
                Step(
                    "Je hoort straks twee liedjes, de een wat hoger dan de andere.", number=1),
                Step("Luister goed, want je kunt ze maar één keer afspelen!", number=2),
                Step(
                    "De toonhoogte is dus anders. Klinkt het toch als hetzelfde liedje?", number=3),
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
                feedback = "Dat klopt! De liedjes zijn inderdaad verschillend."
            else:
                feedback = "Helaas! De liedjes zijn toch echt verschillend."

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
            self.SCORE_CORRECT else "Best lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        debrief_message = "Als je de eerste noten van 'Lang zal ze leven' hoort, herken je het meteen! Hoe kan het dat je dat liedje herkent, zelfs als het veel hoger of langer gezongen wordt? Dit noemen we relatief gehoor. Kijk de filmpjes om uit te vinden hoe dit werkt!"
        body = render_to_string(
            join('info', 'toontjehogerkids', 'debrief.html'),
            {'debrief': debrief_message,
             'vid1': 'https://www.youtube.com/embed/W7EI4JVBs2o?si=rWpjzTi4GiF3XYTz',
             'vid2': 'https://www.youtube.com/embed/UoxcFS6Wds8?si=SXz7XvuIrk30GpXW'})
        info = Info(
            body=body,
            heading="Relatief gehoor",
            button_label="Terug naar ToontjeHogerKids",
            button_link=get_current_collection_url(session)
        )

        return [*score, final, info]
