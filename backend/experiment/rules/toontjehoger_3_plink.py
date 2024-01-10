import logging
from os.path import join
from django.template.loader import render_to_string

from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Explainer, Step, Score, Final, StartSession, Playback, Playlist, Info, Trial
from experiment.actions.form import AutoCompleteQuestion, RadiosQuestion, Form
from .base import Base

from experiment.utils import non_breaking_spaces

from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHoger3Plink(Base):
    ID = 'TOONTJE_HOGER_3_PLINK'
    TITLE = ""
    SCORE_MAIN_CORRECT = 10
    SCORE_MAIN_WRONG = 0
    SCORE_EXTRA_1_CORRECT = 4
    SCORE_EXTRA_2_CORRECT = 4
    SCORE_EXTRA_WRONG = 0

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Muziekherkenning",
            steps=[
                Step("Je krijgt {} zeer korte muziekfragmenten te horen.".format(
                    experiment.rounds)),
                Step("Ken je het nummer? Noem de juiste artiest en titel!"),
                Step(
                    "Weet je het niet? Beantwoord dan extra vragen over de tijdsperiode en emotie van het nummer.")
            ],
            step_numbers=True,
            button_label="Start"
        )

        # 2. Choose playlist.
        playlist = Playlist(experiment.playlists.all())

        # 3. Start session.
        start_session = StartSession()

        return [
            explainer,
            playlist,
            start_session
        ]

    def next_round(self, session, request_session=None):
        """Get action data for the next round"""

        rounds_passed = session.get_relevant_results(['plink']).count()

        # Round 1
        if rounds_passed == 0:
            return self.get_plink_round(session)

        # Round 2-experiments.rounds
        if rounds_passed < session.experiment.rounds:
            return self.get_plink_round(session, present_score=True)

        # Final
        return self.get_final_round(session)

    def get_last_results(self, session):
        ''' get the last score, based on either the main question (plink)
        (only if not skipped)
        or the previous two questions (era and emotion)
        '''
        last_results = session.result_set.order_by('-created_at')[:3]

        if not last_results:
            logger.error("No last result")
            return ""

        if last_results[2].given_response != '':
            # delete other results, because these questions weren't asked
            last_results[0].delete()
            last_results[1].delete()
            return [last_results[2]]

        return last_results[:2]

    def get_score_view(self, session):
        last_results = self.get_last_results(session)
        section = last_results[0].section
        score = sum([r.score for r in last_results])

        if len(last_results) == 1:
            # plink result
            if last_results[0].expected_response == last_results[0].given_response:
                feedback = "Goedzo! Je hoorde inderdaad {} van {}.".format(non_breaking_spaces(section.song.name), non_breaking_spaces(section.song.artist))
            else:
                feedback = "Helaas! Je hoorde {} van {}.".format(non_breaking_spaces(section.song.name), non_breaking_spaces(section.song.artist))
        else:
            if score == 2 * self.SCORE_EXTRA_WRONG:
                feedback_prefix = "Helaas!"
            elif score == self.SCORE_EXTRA_1_CORRECT + self.SCORE_EXTRA_2_CORRECT:
                feedback_prefix = "Goedzo!"
            else:
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
                non_breaking_spaces(section.song.name), non_breaking_spaces(section.song.artist))

            # The \n results in a linebreak
            feedback = "{} {} \n {}".format(
                feedback_prefix, question_part, section_part)

        config = {'show_total_score': True}
        round_number = session.get_relevant_results(['plink']).count() - 1
        score_title =  "Ronde %(number)d / %(total)d" %\
            {'number': round_number+1, 'total': session.experiment.rounds}
        return Score(session, config=config, feedback=feedback, score=score, title=score_title)

    def get_plink_round(self, session, present_score=False):
        next_round = []
        if present_score:
            next_round.append(self.get_score_view(session))
        # Get all song sections
        all_sections = session.all_sections()
        choices = {}
        for section in all_sections:
            label = section.song_label()
            choices[section.pk] = label

        # Get section to recognize
        section = session.section_from_unused_song()
        if section is None:
            raise Exception("Error: could not find section")

        expected_response = section.pk

        question1 = AutoCompleteQuestion(
            key='plink',
            choices=choices,
            question='Noem de artiest en de titel van het nummer',
            result_id=prepare_result(
                'plink',
                session,
                section=section,
                expected_response=expected_response
            )
        )
        next_round.append(Trial(
            playback=Playback(
                player_type='BUTTON',
                sections=[section]
            ),
            feedback_form=Form(
                [question1],
                is_skippable=True,
                skip_label='Ik weet het niet',
                submit_label='Volgende'
            ),
            config={'break_round_on': {'NOT': ['']}}
        ))
        json_data = session.load_json_data()
        if not json_data.get('extra_questions_intro_shown'):
            # Extra questions intro: only show first time
            # --------------------
            extra_questions_intro = Explainer(
                instruction="Tussenronde",
                steps=[
                    Step("Jammer dat je de artiest en titel van dit nummer niet weet!"),
                    Step(
                        "Verdien extra punten door twee extra vragen over het nummer te beantwoorden."),
                ],
                button_label="Start"
            )
            next_round.append(extra_questions_intro)

        extra_rounds = [
            self.get_era_question(session, section),
            self.get_emotion_question(session, section)
        ]

        return [*next_round, *extra_rounds]

    def get_era_question(self, session, section):

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
            result_id=prepare_result(
                'era',
                session,
                section=section,
                expected_response=section.group.split(';')[0]
            )
        )

        return Trial(feedback_form=Form([question]))

    def get_emotion_question(self, session, section):

        # Question
        emotions = ['vrolijk', 'droevig', 'boosheid', 'angst', 'tederheid']
        emotion_choices = {}
        for emotion in emotions:
            emotion_choices[emotion] = emotion.capitalize()

        question = RadiosQuestion(
            question="Welke emotie past bij dit nummer?",
            key='emotion',
            choices=emotion_choices,
            result_id=prepare_result(
                'emotion',
                session,
                section=section,
                expected_response=section.group.split(';')[1]
            )
        )

        return Trial(feedback_form=Form([question]))

    def calculate_score(self, result, data):
        """
        Calculate score, based on the data field
        """
        if result.question_key == 'plink':
            return self.SCORE_MAIN_CORRECT if result.expected_response == result.given_response else self.SCORE_MAIN_WRONG
        elif result.question_key == 'era':
            result.session.save_json_data({'extra_questions_intro_shown': True})
            result.session.save()
            return self.SCORE_EXTRA_1_CORRECT if result.given_response == result.expected_response else self.SCORE_EXTRA_WRONG
        else:
            return self.SCORE_EXTRA_2_CORRECT if result.given_response == result.expected_response else self.SCORE_EXTRA_WRONG

    def get_final_round(self, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score_view(session)

        # Final
        final_text = "Goed gedaan, jouw muziekherkenning is uitstekend!" if session.final_score >= 4 * \
            self.SCORE_MAIN_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment3.html'))
        info = Info(
            body=body,
            heading="Muziekherkenning",
            button_label="Terug naar ToontjeHoger",
            button_link="/toontjehoger"
        )

        return [score, final, info]
