import logging
from django.template.loader import render_to_string
from os.path import join
from experiment.actions.explainer import Explainer, Step
from experiment.actions.final import Final
from experiment.actions.info import Info
from experiment.actions.utils import get_current_experiment_url
from .toontjehoger_1_mozart import toontjehoger_ranks, ToontjeHoger1Mozart

logger = logging.getLogger(__name__)


class ToontjeHogerKids1Mozart(ToontjeHoger1Mozart):
    ID = "TOONTJE_HOGER_KIDS_1_MOZART"

    QUESTION_URL1 = "/images/experiments/toontjehogerkids/mozart-effect1.webp"
    QUESTION_URL2 = "/images/experiments/toontjehogerkids/mozart-effect2.webp"
    ANSWER_URL1 = "/images/experiments/toontjehogerkids/mozart-effect1-answer.webp"
    ANSWER_URL2 = "/images/experiments/toontjehogerkids/mozart-effect2-answer.webp"

    def intro_explaliner(self):
        return Explainer(
            instruction="Het Mozart effect",
            steps=[
                Step("Je hoort zo een kort stukje muziek."),
                Step("Hierna zie je een puzzel."),
                Step("Kun jij het juiste antwoord vinden?"),
            ],
            step_numbers=True,
            button_label="Start",
        )

    def get_task_explainer(self):
        return "Je vouwt een papier en knipt er twee hoekjes af, precies zoals op het plaatje. Welke vorm krijgt het papier dan?"

    def get_final_round(self, session):
        # Finish session.
        session.finish()
        session.save()

        # Answer explainer
        answer_explainer = self.get_answer_explainer(session, round=2)

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
        debrief_message = "Merkte je dat de puzzel beter ging na het \
            horen van Mozart? Dit noemen we het 'Mozart effect'! Wil je meer weten over het Mozart effect? Bekijk dan de filmpjes!"
        body = render_to_string(
            join("info", "toontjehogerkids", "debrief.html"),
            {
                "debrief": debrief_message,
                "vid1": "https://player.vimeo.com/video/1012736186?h=82640b5e3a",
                "vid1_title": "Wat is het Mozart effect?",
                "vid2": "https://player.vimeo.com/video/1012736336?h=e90fff89cd",
                "vid2_title": "Hoe werkt het Mozart effect?",
            },
        )
        info = Info(
            body=body,
            heading="Het Mozart effect",
            button_label="Terug naar ToontjeHogerKids",
            button_link=get_current_experiment_url(session),
        )

        return [*answer_explainer, *score, final, info]
