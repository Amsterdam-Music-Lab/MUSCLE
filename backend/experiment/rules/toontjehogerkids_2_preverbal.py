import logging
from django.template.loader import render_to_string

from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Explainer, Step, Score, Final, Info
from experiment.actions.utils import get_current_experiment_url
from .toontjehoger_2_preverbal import ToontjeHoger2Preverbal
from os.path import join

logger = logging.getLogger(__name__)


class ToontjeHogerKids2Preverbal(ToontjeHoger2Preverbal):
    ID = 'TOONTJE_HOGER_KIDS_2_PREVERBAL'

    def get_intro_explainer(self):
        return Explainer(
            instruction="Het eerste luisteren",
            steps=[
                Step(
                    "Je krijgt straks een soort grafieken van geluid te zien, met een uitlegfilmpje."),
                Step(
                    "Welk plaatje denk jij dat hoort bij de stem van een mens?"),
                Step(
                    "En hoor jij het verschil tussen twee babyhuiltjes?"),
            ],
            step_numbers=True,
            button_label="Start"
        )

    def get_spectrogram_info(self):
        image_url = "/images/experiments/toontjehoger/spectrogram_info_nl.webp"
        description = (
            "Dit is een spectrogram. Wil je weten hoe dat werkt? Kijk dan het filmpje!"
        )
        video = "https://video.leidenuniv.nl/embed/secure/iframe/entryId/1_df3fmqg8/uiConfId/44110401/st/0"
        body = f'<div class="center"><img src="{image_url}"></div><p>{description}</p><iframe width="608" height="402" src="{video}" class="kmsembed" allowfullscreen webkitallowfullscreen mozAllowFullScreen allow="autoplay *; fullscreen *; encrypted-media *" referrerPolicy="no-referrer-when-downgrade" sandbox="allow-downloads allow-forms allow-same-origin allow-scripts allow-top-navigation allow-pointer-lock allow-popups allow-modals allow-orientation-lock allow-popups-to-escape-sandbox allow-presentation allow-top-navigation-by-user-activation" frameborder="0" title="Hoe werkt een spectrogram?"></iframe>'

        # Return answer info view
        info = Info(
            body=body,
            heading="Wat is een spectrogram?",
            button_label="Volgende",
        )
        return info

    def get_score(self, session, rounds_passed):
        # Feedback
        last_result = session.last_result()
        feedback = ""
        if not last_result:
            logger.error("No last result")
            feedback = "Er is een fout opgetreden"
        else:
            if rounds_passed == 1:
                appendix = "Op het volgende scherm kun je de drie geluiden beluisteren."
                if last_result.score == self.SCORE_CORRECT:
                    feedback = "Goedzo! Op plaatje C zie je inderdaad de stem van een mens. " + appendix
                else:
                    feedback = "Helaas! Je antwoord was onjuist. Op plaatje C zag je de stem van een mens. " + appendix
            elif rounds_passed == 2:
                if last_result.score == self.SCORE_CORRECT:
                    feedback = "Goedzo! Geluid A is inderdaad de Franse baby."
                else:
                    feedback = "Helaas! Geluid A is de Franse baby."

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback)
        return [score]

    def get_round1_question(self):
        return "Welk plaatje denk jij dat hoort bij de stem van een mens?"

    def get_round2_question(self):
        return "Hierboven zie je twee spectrogrammen van babyhuiltjes.  Eentje is een Duitse baby en eentje is een Franse baby. De talen Frans en Duits klinken heel anders. Kun jij bedenken welke van deze baby’s de Franse baby is?"

    def get_final_round(self, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session, session.get_rounds_passed())

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
        debrief_message = "Had jij dat gedacht, dat Franse en Duitse baby's anders huilen? Waarom zouden ze dat doen denk je? Bekijk de filmpjes om dit uit te vinden!"
        body = render_to_string(
            join("info", "toontjehogerkids", "debrief.html"),
            {
                "debrief": debrief_message,
                "vid1": "https://video.leidenuniv.nl/embed/secure/iframe/entryId/1_q8r74zji/uiConfId/4411040 1/st/0",
                "vid1_title": "Franse en Duitse baby",
                "vid2": "https://video.leidenuniv.nl/embed/secure/iframe/entryId/1_rteiyere/uiConfId/4411040 1/st/0",
                "vid2_title": "Geluiden in Duitsland en Frankrijk",
            },
        )
        info = Info(
            body=body,
            heading="Het eerste luisteren",
            button_label="Terug naar ToontjeHogerKids",
            button_link=get_current_experiment_url(session)
        )

        return [*score, final, info]
