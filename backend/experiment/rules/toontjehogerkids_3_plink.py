import logging
from os.path import join
from django.template.loader import render_to_string

from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Explainer, Step, Score, Final, Info, Trial
from experiment.actions.playback import PlayButton
from experiment.actions.form import AutoCompleteQuestion, Form
from .toontjehoger_3_plink import ToontjeHoger3Plink

from experiment.utils import non_breaking_spaces

from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHogerKids3Plink(ToontjeHoger3Plink):
    ID = 'TOONTJE_HOGER_KIDS_3_PLINK'
    TITLE = ""
    SCORE_MAIN_CORRECT = 10
    SCORE_MAIN_WRONG = 0
    SCORE_EXTRA_1_CORRECT = 4
    SCORE_EXTRA_2_CORRECT = 4
    SCORE_EXTRA_WRONG = 0

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""

        explainer = Explainer(
            instruction="Muziekherkenning",
            steps=[
                Step("Je hoort zo een heel kort stukje van een liedje.".format(
                    experiment.rounds)),
                Step("Herken je dit liedje? Kies dan de juiste artiest en titel!"),
                Step(
                    "Weet je het niet zeker? Doe dan maar een gok.")
            ],
            step_numbers=True,
            button_label="Start"
        )

        return [
            explainer
        ]

    def get_last_result(self, session):
        ''' get the last score, based on question (plink)
        '''
        last_result = session.result_set.last()

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
                non_breaking_spaces(section.song.name), non_breaking_spaces(section.song.artist))
        else:
            feedback = "Helaas! Je hoorde {} van {}.".format(non_breaking_spaces(
                section.song.name), non_breaking_spaces(section.song.artist))

        config = {'show_total_score': True}
        round_number = session.get_relevant_results(['plink']).count() - 1
        score_title = "Ronde %(number)d / %(total)d" %\
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
            question='Kies de artiest en de titel van het nummer',
            result_id=prepare_result(
                'plink',
                session,
                section=section,
                expected_response=expected_response
            )
        )
        next_round.append(Trial(
            playback=PlayButton(
                sections=[section]
            ),
            feedback_form=Form(
                [question1],
                submit_label='Volgende'
            )
        ))
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
        final_text = "Goed gedaan!" if session.final_score >= 4 * \
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
