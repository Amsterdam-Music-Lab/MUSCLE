import logging
from django.template.loader import render_to_string
from os.path import join
from section.models import Playlist
from experiment.actions import Trial, Explainer, Step, Score, Final, Info, HTML
from experiment.actions.form import ButtonArrayQuestion, Form
from experiment.actions.playback import Autoplay
from experiment.actions.styles import ColorScheme
from experiment.models import Session
from .base import BaseRules
from experiment.utils import non_breaking_spaces
from experiment.actions.utils import get_current_experiment_url

from result.utils import prepare_result

logger = logging.getLogger(__name__)


def toontjehoger_ranks(session):
    score = session.final_score
    if score < 25:
        return "PLASTIC"
    elif score < 50:
        return "BRONZE"
    elif score < 75:
        return "SILVER"
    else:
        return "GOLD"


class ToontjeHoger1Mozart(BaseRules):
    ID = "TOONTJE_HOGER_1_MOZART"
    TITLE = ""
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    QUESTION_URL1 = "/images/experiments/toontjehoger/mozart-effect1.webp"
    QUESTION_URL2 = "/images/experiments/toontjehoger/mozart-effect2.webp"
    ANSWER_URL1 = "/images/experiments/toontjehoger/mozart-effect1-answer.webp"
    ANSWER_URL2 = "/images/experiments/toontjehoger/mozart-effect2-answer.webp"

    def next_round(self, session: Session):
        """Get action data for the next round"""
        rounds_passed = session.get_rounds_passed()

        # Round 1
        # 1. Explain game.
        explainer = Explainer(
            instruction="Het Mozart effect",
            steps=[
                Step("Je hoort een muziekfragment van ongeveer 25 seconden."),
                Step("Hierna verschijnt een korte puzzel."),
                Step("Lukt het om het juiste antwoord te vinden?"),
            ],
            step_numbers=True,
            button_label="Start",
        )

        if rounds_passed == 0:
            round = self.get_image_trial(
                session,
                section_group="1",
                image_url=self.QUESTION_URL1,
                question=self.get_task_explainer(),
                expected_response="B",
            )
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return [explainer, *round]

        # Round 2
        if rounds_passed == 1:
            answer_explainer = self.get_answer_explainer(session, round=1)
            score = self.get_score(session)
            round = self.get_image_trial(
                session,
                section_group="2",
                image_url=self.QUESTION_URL2,
                question=self.get_task_explainer(),
                expected_response="B",
            )
            return [*answer_explainer, *score, *round]

        # Final
        return self.get_final_round(session)

    def get_task_explainer(self):
        return "Welke vorm ontstaat er na het afknippen van de hoekjes?"

    def get_answer_explainer(self, session, round):
        last_result = session.last_result()

        correct_answer_given = last_result.score > 0

        heading = "Goed gedaan!" if correct_answer_given else "Helaas!"

        feedback_correct = "Het juiste antwoord was inderdaad {}.".format(last_result.expected_response)
        feedback_incorrect = "Antwoord {} is niet goed! Het juiste antwoord was {}.".format(
            last_result.given_response, last_result.expected_response
        )
        feedback = feedback_correct if correct_answer_given else feedback_incorrect

        image_url = self.ANSWER_URL1 if round == 1 else self.ANSWER_URL2
        body = '<div class="center"><div><img src="{}"></div><h4 style="margin-top: 15px;">{}</h4></div>'.format(
            image_url, feedback
        )

        # Return answer info view
        info = Info(
            body=body,
            heading=heading,
            button_label="Volgende",
        )
        return [info]

    def get_score(self, session):
        # Feedback message
        last_result = session.last_result()
        section = last_result.section
        feedback = "Je hoorde {} van {}.".format(section.song.name, section.artist_name()) if section else ""

        # Return score view
        config = {"show_total_score": True}
        score = Score(session, config=config, feedback=feedback)
        return [score]

    def get_image_trial(self, session, section_group, image_url, question, expected_response):
        # Config
        # -----------------
        section = session.playlist.get_section(filter_by={"group": section_group})
        if section is None:
            raise Exception("Error: could not find section")

        # Step 1
        # --------------------

        # Listen
        playback = Autoplay([section], show_animation=True)

        listen_config = {
            "auto_advance": True,
            "show_continue_button": False,
            "response_time": section.duration,
        }

        listen = Trial(
            config=listen_config,
            playback=playback,
            title=self.TITLE,
        )

        # Step 2
        # --------------------

        # Question
        key = "expected_shape"
        question = ButtonArrayQuestion(
            question=question,
            key=key,
            choices={
                "A": "A",
                "B": "B",
                "C": "C",
                "D": "D",
                "E": "E",
            },
            view="BUTTON_ARRAY",
            result_id=prepare_result(
                key, session, section=section, expected_response=expected_response
            ),
            submits=True,
            style=[ColorScheme.TOONTJEHOGER],
        )
        form = Form([question])

        image_trial = Trial(
            html=HTML(body='<img src="{}" style="max-height:326px;max-width: 100%;"/>'.format(image_url)),
            feedback_form=form,
            title=self.TITLE,
        )

        return [listen, image_trial]

    def get_explainer_round2():
        explainer = Explainer(
            instruction="Het Mozart effect",
            steps=[
                Step("Je krijgt nu een ander muziekfragment van 20 seconden te horen."),
                Step("Hierna verschijnt weer een korte puzzel."),
                Step("Lukt het nu om de juiste te kiezen?"),
            ],
            step_numbers=True,
            button_label="Start",
        )

        return [explainer]

    def calculate_score(self, result, data):
        score = self.SCORE_CORRECT if result.expected_response == result.given_response else self.SCORE_WRONG
        return score

    def get_final_round(self, session):
        # Finish session.
        session.finish()
        session.save()

        # Answer explainer
        answer_explainer = self.get_answer_explainer(session, round=2)

        # Score
        score = self.get_score(session)

        # Final
        final_text = (
            "Je hebt het uitstekend gedaan!"
            if session.final_score >= 2 * self.SCORE_CORRECT
            else "Dat bleek toch even lastig!"
        )
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={"text": "Wat hebben we getest?"},
        )

        # Info page
        body = render_to_string(join("info", "toontjehoger", "experiment1.html"))
        info = Info(
            body=body,
            heading="Het Mozart effect",
            button_label="Terug naar ToontjeHoger",
            button_link=get_current_experiment_url(session),
        )

        return [*answer_explainer, *score, final, info]

    def validate_playlist(self, playlist: Playlist):
        errors = []

        errors += super().validate_playlist(playlist)

        # Check if playlist has 2 sections
        if playlist.section_set.count() != 2:
            errors.append("The playlist should have 2 sections")

        # Check if sections have different groups
        groups = [section.group for section in playlist.section_set.all()]
        if len(set(groups)) != 2:
            errors.append("The sections should have different groups")

        # Check if sections have group 1 and 2
        if sorted(groups) != ["1", "2"]:
            errors.append("The sections should have groups 1 and 2")

        return errors
