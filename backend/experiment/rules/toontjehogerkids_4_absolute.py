from os.path import join
from django.template.loader import render_to_string
from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Explainer, Step, Final, Info
from .toontjehoger_4_absolute import ToontjeHoger4Absolute



class ToontjeHogerKids4Absolute(ToontjeHoger4Absolute):
    ID = 'TOONTJE_HOGER_KIDS_4_ABSOLUTE'
    PLAYLIST_ITEMS = 13

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Absoluut gehoor",
            steps=[
                Step(
                    "Je gaat zo luisteren naar stukjes muziek die je misschien herkent van een tv-programma of filmpje."),
                Step(
                    "Je kunt steeds twee versies luisteren. Eén hiervan is het origineel. De andere hebben we een beetje hoger of lager gemaakt."),
                Step("Kan jij horen welke van de twee versies precies zo hoog of laag is als je 'm kent? Welke is het origineel?"),
            ],
            step_numbers=True,
            button_label="Start"
        )

        return [
            explainer,
        ]

    def get_trial_question(self):
        return "Welke van deze twee stukjes muziek klinkt precies zo hoog of laag als in het echt?"
 
    def get_final_round(self, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session)

        # Final
        final_text = "Dat bleek toch even lastig!"
        if session.final_score >= session.experiment.rounds * 0.5 * self.SCORE_CORRECT:
            final_text = "Goed gedaan!"

        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        debrief_message = "Lukte het jou om het juiste antwoord te kiezen? Dan heb je goed onthouden hoe hoog of laag die muziekjes normaal altijd klinken! Sommige mensen noemen dit absoluut gehoor. \
            Is dat eigenlijk bijzonder? Kijk de filmpjes om daar achter te komen!"
        body = render_to_string(
            join('info', 'toontjehogerkids', 'debrief.html'),
            {'debrief': debrief_message, 'vid1': 'https://www.youtube.com/embed/0wpT-wjI-0M?si=CALvWqid4SjabL9S',
             'vid2': 'https://www.youtube.com/embed/LQnl1OP3q_Q?si=yTDVPnR7BAeBqWph'})
        info = Info(
            body=body,
            heading="Absoluut gehoor",
            button_label="Terug naar ToontjeHoger",
            button_link="/collection/thkids"
        )

        return [*score, final, info]
