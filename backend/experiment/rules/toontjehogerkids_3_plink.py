import logging
from os.path import join
from django.template.loader import render_to_string

from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Explainer, Step, Score, Final, Info, Trial
from experiment.actions.playback import PlayButton
from experiment.actions.form import DropdownQuestion, Form
from experiment.actions.utils import get_current_experiment_url
from experiment.utils import non_breaking_spaces
from .toontjehoger_3_plink import ToontjeHoger3Plink
from section.models import Section
from session.models import Session


from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHogerKids3Plink(ToontjeHoger3Plink):
    ID = "TOONTJE_HOGER_KIDS_3_PLINK"
    TITLE = ""
    SCORE_MAIN_CORRECT = 10
    SCORE_MAIN_WRONG = 0
    SCORE_EXTRA_1_CORRECT = 4
    SCORE_EXTRA_2_CORRECT = 4
    SCORE_EXTRA_WRONG = 0

    def validate_era_and_mood(self, sections):
        return []

    def get_intro_explainer(self, n_rounds):
        return Explainer(
            instruction="Muziekherkenning",
            steps=[
                Step("Je hoort zo een heel kort stukje van {} liedjes.".format(n_rounds)),
                Step("Herken je de liedjes? Kies dan steeds de juiste artiest en titel!"),
                Step("Weet je het niet zeker? Doe dan maar een gok."),
                Step("Herken jij er meer dan 3?"),
            ],
            step_numbers=True,
            button_label="Start",
        )

    def get_last_result(self, session):
        """get the last score, based on question (plink)"""
        last_result = session.last_result()

        if not last_result:
            logger.error("No last result")
            return ""

        return last_result

    def get_score_view(self, session):
        last_result = self.get_last_result(session)
        section = last_result.section
        score = last_result.score

        if last_result.expected_response == last_result.given_response:
            feedback = "Goedzo! Je hoorde inderdaad {} van {}.".format(
                non_breaking_spaces(section.song_name()),
                non_breaking_spaces(section.artist_name()),
            )
        else:
            feedback = "Helaas! Je hoorde {} van {}.".format(
                non_breaking_spaces(section.song_name()),
                non_breaking_spaces(section.artist_name()),
            )

        config = {"show_total_score": True}
        round_number = session.get_rounds_passed()
        score_title = "Ronde %(number)d / %(total)d" % {"number": round_number, "total": session.block.rounds}
        return Score(session, config=config, feedback=feedback, score=score, title=score_title)

    def get_plink_trials(self, session: Session, section: Section, choices: dict, expected_response: str) -> list:
        next_round = []
        question1 = DropdownQuestion(
            key="plink",
            choices=choices,
            question="Kies de artiest en de titel van het nummer",
            result_id=prepare_result("plink", session, section=section, expected_response=expected_response),
        )
        next_round.append(
            Trial(playback=PlayButton(sections=[section]), feedback_form=Form([question1], submit_label="Volgende"))
        )
        return next_round

    def calculate_score(self, result, data):
        """
        Calculate score, based on the data field
        """
        return self.SCORE_MAIN_CORRECT if result.expected_response == result.given_response else self.SCORE_MAIN_WRONG

    def get_final_round(self, session):
        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score_view(session)

        # Final
        final_text = "Goed gedaan!" if session.final_score >= 4 * self.SCORE_MAIN_CORRECT else "Best lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={"text": "Wat hebben we getest?"},
        )

        # Info page
        debrief_message = "Hoe snel denk je dat je een popliedje kunt herkennen? Binnen tien seconden?\
            Binnen twee seconden? Of nog minder? Kijk de filmpjes voor het antwoord!"
        body = render_to_string(
            join("info", "toontjehogerkids", "debrief.html"),
            {
                "debrief": debrief_message,
                "vid1": "https://player.vimeo.com/video/1012062402?h=342dd7ab90",
                "vid1_title": "Super snel liedjes herkennen!",
                "vid2": "https://player.vimeo.com/video/1012062961?h=bf5749901d",
                "vid2_title": "Kun je elk liedje zo snel herkennen?",
            },
        )
        info = Info(
            body=body,
            heading="Muziekherkenning",
            button_label="Terug naar ToontjeHogerKids",
            button_link=get_current_experiment_url(session),
        )

        return [score, final, info]
