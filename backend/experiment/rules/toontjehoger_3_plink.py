import logging
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from .views import Plink, Explainer, Step, Score, Final, StartSession, Playlist, Info
from .views.form import RadiosQuestion
from .base import Base
from os.path import join
from .util.actions import combine_actions
from .util.strings import non_breaking

logger = logging.getLogger(__name__)


class ToontjeHoger3Plink(Base):
    ID = 'TOONTJE_HOGER_3_PLINK'
    TITLE = ""
    SCORE_MAIN_CORRECT = 4
    SCORE_MAIN_WRONG = 0
    SCORE_EXTRA_1_CORRECT = 2
    SCORE_EXTRA_2_CORRECT = 1
    SCORE_EXTRA_WRONG = 0

    @classmethod
    def first_round(cls, experiment, participant):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Muziekherkenning",
            steps=[
                Step("Luister naar een zeer kort muziekfragment."),
                Step("Ken je het nummer? Noem de juiste artiest en titel!"),
                Step(
                    "Weet je het niet? Beantwoord dan extra vragen over de tijdsperiode en emotie van het nummer.")
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
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return cls.get_plink_round(session)

        # Round 2-experiments.rounds
        if rounds_passed < session.experiment.rounds:
            return combine_actions(*cls.get_score(session), *cls.get_plink_round(session))

        # Final
        return combine_actions(*cls.get_final_round(session))

    @classmethod
    def get_score_message(cls, session):
        last_result = session.last_result()

        if not last_result:
            logger.error("No last result")
            return ""

        data = last_result.load_json_data()

        # Section
        section = last_result.section
        if not section:
            logger.error("Result without section")
            return ""

        # Option 1. Main question
        main_question = Plink.extract_main_question(data)

        if main_question:
            if main_question == last_result.expected_response:
                return "Goedzo! Je hoorde inderdaad {} van {}.".format(non_breaking(section.name), non_breaking(section.artist))

            return "Helaas! Je hoorde {} van {}.".format(non_breaking(section.name), non_breaking(section.artist))

        # Option 2. Extra questions
        extra_questions = Plink.extract_extra_questions(data)

        # No extra questions? Return just an empty string
        if not extra_questions:
            return ""

        # Feedback prefix

        # - All points
        feedback_prefix = "Goedzo!"

        # - Partial score or all questions wrong
        all_wrong_score = last_result.score == 2 * cls.SCORE_EXTRA_WRONG
        only_half_score = last_result.score < cls.SCORE_EXTRA_1_CORRECT + \
            cls.SCORE_EXTRA_2_CORRECT if not all_wrong_score else False

        if all_wrong_score:
            feedback_prefix = "Helaas!"
        elif only_half_score:
            feedback_prefix = "Deels goed!"

        # Get section info
        section_details = section.group.split(";")
        time_period = section_details[0] if len(
            section_details) >= 1 else "?"
        time_period = time_period.replace("s", "'s")
        emotion = section_details[1] if len(section_details) >= 2 else "?"

        # Construct final feedback message
        question_part = "Het nummer komt uit de {} en de emotie is {}.".format(
            time_period, emotion)
        section_part = "Je hoorde {} van {}.".format(
            non_breaking(section.name), non_breaking(section.artist))

        # The \n results in a linebreak
        feedback = "{} {} \n {}".format(
            feedback_prefix, question_part, section_part)
        return feedback

    @classmethod
    def get_score(cls, session):
        feedback = cls.get_score_message(session)

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback).action()

        return [score]

    @classmethod
    def get_plink_round(cls, session):

        # Config
        # -----------------

        # Get all song sections
        all_sections = session.all_sections()
        choices = {}
        for section in all_sections:
            label = section.song_label()
            choices[section.pk] = label

        # Get section to recognize
        section = session.section_from_unused_song()
        if section == None:
            raise Exception("Error: could not find section")

        expected_response = section.pk
        result_pk = cls.prepare_result(
            session, section=section, expected_response=expected_response)

        # Extra questions intro
        # --------------------
        extra_questions_intro = Explainer(
            instruction="Tussenronde",
            steps=[
                Step("Jammer dat je de artiest en titel van dit nummer niet weet!"),
                Step(
                    "Verdien extra punten door twee extra vragen over het nummer te beantwoorden."),
            ],
            button_label="Start"

        ).action(step_numbers=False)

        # Plink round
        # --------------------
        extra_questions = [cls.get_optional_question1(
            session), cls.get_optional_question2(session)]

        plink = Plink(
            section=section,
            title=cls.TITLE,
            result_id=result_pk,
            main_question="Noem de artiest en de titel van het nummer",
            choices=choices,
            submit_label="Volgende",
            dont_know_label="Ik weet het niet",
            extra_questions=extra_questions,
            extra_questions_intro=extra_questions_intro
        ).action()

        return [plink]

    @classmethod
    def get_optional_question1(cls, session):

        # Config
        # -----------------

        # Question
        periods = ["60's", "70's", "80's", "90's", "00's", "10's", "20's"]
        period_choices = {}
        for period in periods:
            period_choices[period.replace("'", "")] = period

        question = RadiosQuestion(
            question="Wanneer is het nummer uitgebracht?",
            key='time_period',
            choices=period_choices,
            submits=False
        )

        return question.action()

    @classmethod
    def get_optional_question2(cls, session):

        # Question
        emotions = ['vrolijk', 'droevig', 'boosheid', 'angst', 'tederheid']
        emotion_choices = {}
        for emotion in emotions:
            emotion_choices[emotion] = emotion.capitalize()

        question = RadiosQuestion(
            question="Welke emotie past bij dit nummer?",
            key='emotion',
            choices=emotion_choices,
            submits=True
        )

        return question.action()

    @classmethod
    def calculate_score(cls, result, data):
        """
        Calculate score, based on the data field

        e.g. only main question answered
        {
            main_question: "100",
            extra_questions: []
        }

        e.g. only main question answered
        {
            main_question: "",
            extra_questions: ["60s","vrolijk"]
        }

        """
        main_question = Plink.extract_main_question(data)

        # Participant guessed the artist/title:
        if main_question != "":
            result.given_response = main_question
            result.save()
            return cls.SCORE_MAIN_CORRECT if result.expected_response == result.given_response else cls.SCORE_MAIN_WRONG

        # Handle extra questions data
        extra_questions = Plink.extract_extra_questions(data)
        if extra_questions:
            section = result.section
            if section is None:
                logger.error("Error: No section on result")
                return 0

            score = 0

            # Check if the given answers
            # e.g section.group = 60s;vrolijk (time_period;emotion)
            for index, answer in enumerate(extra_questions):
                points_correct = cls.SCORE_EXTRA_1_CORRECT if index == 0 else cls.SCORE_EXTRA_2_CORRECT
                score += points_correct if answer and (
                    answer in section.group) else cls.SCORE_EXTRA_WRONG

            return score

        # Should not happen
        logger.error("Error: could not calculate score")
        return 0

    @classmethod
    def get_final_round(cls, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = cls.get_score(session)

        # Final
        final_text = "Goed gedaan, jouw muziekherkenning is uitstekend!" if session.final_score >= 4 * \
            cls.SCORE_MAIN_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=cls.rank(session),
            button={'text': 'Wat hebben we getest?'}
        ).action()

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment3.html'))
        info = Info(
            body=body,
            heading="Muziekherkenning",
            button_label="Terug naar ToontjeHoger",
            button_link="/toontjehoger"
        ).action()

        return [*score, final, info]
