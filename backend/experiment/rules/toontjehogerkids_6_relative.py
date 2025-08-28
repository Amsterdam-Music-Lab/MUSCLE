import logging
from os.path import join

from django.template.loader import render_to_string

from experiment.actions.explainer import Explainer, Step
from experiment.actions.final import Final
from experiment.actions.score import Score
from experiment.actions.utils import get_current_experiment_url
from .toontjehoger_1_mozart import toontjehoger_ranks
from .toontjehoger_6_relative import ToontjeHoger6Relative

logger = logging.getLogger(__name__)


class ToontjeHogerKids6Relative(ToontjeHoger6Relative):
    ID = "TOONTJE_HOGER_KIDS_6_RELATIVE"

    def get_intro_explainer(self):
        return Explainer(
            instruction="Relatief Gehoor",
            steps=[
                Step("In dit testje kun je jouw relatief gehoor testen!"),
                # Empty step adds some spacing between steps to improve readability
                Step(""),
                Step("Je hoort straks twee liedjes, de een wat hoger dan de andere.", number=1),
                Step("Luister goed, want je kunt ze maar één keer afspelen!", number=2),
                Step("De toonhoogte is dus anders. Klinkt het toch als hetzelfde liedje?", number=3),
            ],
            button_label="Start",
        )

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
        config = {"show_total_score": True}
        score = Score(session, config=config, feedback=feedback)
        return [score]

    def get_final_round(self, session):
        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session)

        # Final
        final_text = "Goed gedaan!" if session.final_score >= 2 * self.SCORE_CORRECT else "Best lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={"text": "Wat hebben we getest?"},
        )

        # Info page
        debrief_message = "Als je de eerste noten van 'Lang zal ze leven' hoort, herken je het meteen! Hoe kan het dat je dat liedje herkent, zelfs als het veel hoger of lager gezongen wordt? Dit noemen we relatief gehoor. Kijk de filmpjes om uit te vinden hoe dit werkt!"
        body = render_to_string(
            join("info", "toontjehogerkids", "debrief.html"),
            {
                "debrief": debrief_message,
                "vid1": "https://player.vimeo.com/video/1012736436?h=11b7974f13",
                "vid1_title": "Relatief gehoor, wat is dat?",
                "vid2": "https://player.vimeo.com/video/1012736666?h=b1098b4bbb",
                "vid2_title": "Relatief gehoor en toonladders",
            },
        )
        info = Info(
            body=body,
            heading="Relatief gehoor",
            button_label="Terug naar ToontjeHogerKids",
            button_link=get_current_experiment_url(session),
        )

        return [*score, final, info]
