from os.path import join
from django.template.loader import render_to_string

from experiment.actions.explainer import Explainer, Step
from experiment.actions.final import Final
from experiment.actions.info import Info
from experiment.actions.utils import get_current_experiment_url
from .toontjehoger_1_mozart import toontjehoger_ranks
from .toontjehoger_4_absolute import ToontjeHoger4Absolute


class ToontjeHogerKids4Absolute(ToontjeHoger4Absolute):
    ID = "TOONTJE_HOGER_KIDS_4_ABSOLUTE"
    PLAYLIST_ITEMS = 12

    def get_intro_explainer(self):
        return Explainer(
            instruction="Absoluut gehoor",
            steps=[
                Step("Je hoort straks stukjes muziek van televisie of filmpjes."),
                Step(
                    "Het zijn er steeds twee: Eentje is het origineel, de andere hebben we een beetje hoger of lager gemaakt."
                ),
                Step("Welke klinkt precies zoals jij 'm kent? Welke is het origineel?"),
            ],
            step_numbers=True,
            button_label="Start",
        )

    def get_trial_question(self):
        return "Welke van deze twee stukjes muziek klinkt precies zo hoog of laag als jij 'm kent?"

    def get_final_round(self, session):
        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session)

        # Final
        final_text = "Best lastig!"
        if session.final_score >= session.block.rounds * 0.5 * self.SCORE_CORRECT:
            final_text = "Goed gedaan!"

        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={"text": "Wat hebben we getest?"},
        )

        # Info page
        debrief_message = (
            "Lukte het jou om het juiste antwoord te kiezen? Dan heb je goed onthouden hoe hoog of laag die muziekjes normaal altijd klinken! Sommige mensen noemen dit absoluut gehoor. \
            Is dat eigenlijk bijzonder? Kijk de filmpjes om daar achter te komen!"
        )
        body = render_to_string(
            join("info", "toontjehogerkids", "debrief.html"),
            {
                "debrief": debrief_message,
                "vid1": "https://player.vimeo.com/video/1012705794?h=f8aa6548a9",
                "vid1_title": "Absoluut gehoor, wat betekent dat?",
                "vid2": "https://player.vimeo.com/video/1012705982?h=a37c718512",
                "vid2_title": "Is een absoluut gehoor bijzonder?",
            },
        )
        info = Info(
            body=body,
            heading="Absoluut gehoor",
            button_label="Terug naar ToontjeHogerKids",
            button_link=get_current_experiment_url(session),
        )

        return [*score, final, info]
