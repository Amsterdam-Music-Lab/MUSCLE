import logging
from django.template.loader import render_to_string

from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Explainer, Step, Score, Final, Info
from .toontjehoger_2_preverbal import ToontjeHoger2Preverbal
from os.path import join

logger = logging.getLogger(__name__)


class ToontjeHogerKids2Preverbal(ToontjeHoger2Preverbal):
    ID = 'TOONTJE_HOGER_KIDS_2_PREVERBAL'

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
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

        # 2 Spectrogram information
        spectrogram_info = self.get_spectrogram_info()

        return [
            explainer,
            spectrogram_info,
        ]

    def get_spectrogram_info(self):
        image_url = "/images/experiments/toontjehoger/spectrogram_info_nl.webp"
        description = "Dit is een spectogram. Wil je weten hoe dat werkt? Kijk dan het filmpje!"
        video = 'https://www.youtube.com/embed/Mw5u3fe9aMI?si=lWc7xFpoj4gBZj2d'
        body = f'<div class="center"><img src="{image_url}"></div><p>{description}</p><iframe width="100%" height="315" src={video}></iframe>'

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
        score = self.get_score(session, session.rounds_passed())

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
            join('info', 'toontjehogerkids', 'debrief.html'),
            {'debrief': debrief_message, 'vid1': 'https://www.youtube.com/embed/q7L_vwB7eIo?si=mRVJKE2urKT-Xxft',
             'vid2': 'https://www.youtube.com/embed/4eKcwGB6xmc?si=ogeEhtyEFa9WxP9i'})
        info = Info(
            body=body,
            heading="Het eerste luisteren",
            button_label="Terug naar ToontjeHogerKids",
            button_link="/collection/thkids"
        )

        return [*score, final, info]
