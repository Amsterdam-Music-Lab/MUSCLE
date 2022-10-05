import logging
from django.template.loader import render_to_string
from os.path import join
from .views import Trial, Explainer, Step, Score, Final, StartSession, Playlist, Info, HTML
from .views.form import ButtonArrayQuestion, Form
from .views.playback import Playback
from .base import Base
from .util.actions import combine_actions
from .util.strings import non_breaking

logger = logging.getLogger(__name__)

QUESTION_URL1 = "/images/experiments/toontjehoger/mozart-effect1.webp"
QUESTION_URL2 = "/images/experiments/toontjehoger/mozart-effect2.webp"
ANSWER_URL1 = "/images/experiments/toontjehoger/mozart-effect1-answer.webp"
ANSWER_URL2 = "/images/experiments/toontjehoger/mozart-effect2-answer.webp"


class ToontjeHoger1Mozart(Base):
    ID = 'TOONTJE_HOGER_1_MOZART'
    TITLE = ""
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    @classmethod
    def first_round(cls, experiment, participant):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Het Mozart effect",
            steps=[
                Step("Je hoort een muziekfragment van ongeveer 25 seconden."),
                Step("Hierna verschijnt een korte puzzel."),
                Step("Lukt het om het juiste antwoord te vinden?"),
            ],
            button_label="Start"
        ).action(step_numbers=True)

        # 2. Choose playlist.
        playlist = Playlist.action(experiment.playlists.all())

        # 3. Start session.
        start_session = StartSession.action()

        return [
            explainer,
            playlist,
            start_session
        ]

    @classmethod
    def next_round(cls, session, request_session=None):
        """Get action data for the next round"""
        rounds_passed = session.rounds_passed()

        # Round 1
        if rounds_passed == 0:
            round = cls.get_image_trial(session,
                                        section_group='1',
                                        image_url=QUESTION_URL1,
                                        question="Welke vorm ontstaat er na het afknippen van de hoekjes?",
                                        expected_response='B'
                                        )
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return round

        # Round 2
        if rounds_passed == 1:
            answer_explainer = cls.get_answer_explainer(session, round=1)
            score = cls.get_score(session)
            round = cls.get_image_trial(session,
                                        section_group='2',
                                        image_url=QUESTION_URL2,
                                        question="Welke vorm ontstaat er na het afknippen van het hoekje?",
                                        expected_response='B'
                                        )
            return combine_actions(*answer_explainer, *score, *round)

        # Final
        return combine_actions(*cls.get_final_round(session))

    @classmethod
    def get_answer_explainer(cls, session, round):
        last_result = session.last_result()

        correct_answer_given = last_result.score > 0

        heading = "Goed gedaan!" if correct_answer_given else "Helaas!"

        feedback_correct = "Het juiste antwoord was inderdaad {}.".format(
            last_result.expected_response)
        feedback_incorrect = "Antwoord {} is niet goed! Het juiste antwoord was {}.".format(
            last_result.given_response, last_result.expected_response)
        feedback = feedback_correct if correct_answer_given else feedback_incorrect

        image_url = ANSWER_URL1 if round == 1 else ANSWER_URL2
        body = '<div class="center"><div><img src="{}"></div><h4 style="margin-top: 15px;">{}</h4></div>'.format(
            image_url, feedback)

        # Return answer info view
        info = Info(
            body=body,
            heading=heading,
            button_label="Volgende",
        ).action()
        return [info]

    @classmethod
    def get_score(cls, session):
        # Feedback message
        last_result = session.last_result()
        section = last_result.section
        feedback = "Je hoorde {} van {}.".format(
            section.name, non_breaking(section.artist)) if section else ""

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback).action()
        return [score]

    @classmethod
    def get_image_trial(cls, session, section_group, image_url, question, expected_response):
        # Config
        # -----------------
        section = session.section_from_any_song(
            filter_by={'group': section_group})
        if section == None:
            raise Exception("Error: could not find section")

        result_pk = cls.prepare_result(
            session, section=section, expected_response=expected_response)

        # Step 1
        # --------------------

        # Listen
        play_config = {'show_animation': True}
        playback = Playback([section],
                            player_type=Playback.TYPE_AUTOPLAY,
                            play_config=play_config
                            )

        listen_config = {
            'auto_advance': True,
            'show_continue_button': False,
            'decision_time': section.duration
        }

        listen = Trial(
            config=listen_config,
            playback=playback,
            title=cls.TITLE,
        ).action()

        # Step 2
        # --------------------

        # Question
        question = ButtonArrayQuestion(
            question=question,
            key='expected_shape',
            choices={
                'A': 'A',
                'B': 'B',
                'C': 'C',
                'D': 'D',
                'E': 'E',
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        form = Form([question])

        image_trial = HTML(
            html='<img src="{}" style="height:calc(100% - 260px);max-height:326px;max-width: 100%;"/>'.format(
                image_url),
            form=form,
            title=cls.TITLE,
            result_id=result_pk
        ).action()

        return [listen, image_trial]

    @classmethod
    def get_explainer_round2():
        explainer = Explainer(
            instruction="Het Mozart effect",
            steps=[
                Step("Je krijgt nu een ander muziekfragment van 20 seconden te horen."),
                Step("Hierna verschijnt weer een korte puzzel."),
                Step("Lukt het nu om de juiste te kiezen?"),
            ],
            button_label="Start"
        ).action(step_numbers=True)

        return [explainer]

    @classmethod
    def calculate_score(cls, result, data, form_element):
        score = cls.SCORE_CORRECT if result.expected_response == result.given_response else cls.SCORE_WRONG
        return score

    @classmethod
    def get_final_round(cls, session):

        # Finish session.
        session.finish()
        session.save()

        # Answer explainer
        answer_explainer = cls.get_answer_explainer(session, round=2)

        # Score
        score = cls.get_score(session)

        # Final
        final_text = "Je hebt het uitstekend gedaan!" if session.final_score >= 2 * \
            cls.SCORE_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=cls.rank(session),
            button={'text': 'Wat hebben we getest?'}
        ).action()

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment1.html'))
        info = Info(
            body=body,
            heading="Het Mozart effect",
            button_label="Terug naar ToontjeHoger",
            button_link="/toontjehoger"
        ).action()

        return [*answer_explainer, *score, final, info]
