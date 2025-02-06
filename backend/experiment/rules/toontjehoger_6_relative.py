import logging
from django.template.loader import render_to_string
from os.path import join

from experiment.actions import Trial, Explainer, Step, Score, Final, Info
from experiment.actions.form import ChoiceQuestion, Form
from experiment.actions.playback import Multiplayer
from experiment.actions.styles import ColorScheme
from experiment.actions.utils import get_current_experiment_url
from section.models import Playlist
from session.models import Session
from .base import BaseRules
from .toontjehoger_1_mozart import toontjehoger_ranks

from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHoger6Relative(BaseRules):
    ID = 'TOONTJE_HOGER_6_RELATIVE'
    TITLE = ""
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    def validate_playlist(self, playlist: Playlist):
        ''' This is the original Toontjehoger6Relative playlist:
        ```
        AML,Fragment A,0.0,1.0,/toontjehoger/relative/relative_a.mp3,a,0
        AML,Fragment B,0.0,1.0,/toontjehoger/relative/relative_b.mp3,b,0
        AML,Fragment C,0.0,1.0,/toontjehoger/relative/relative_c.mp3,c,0
        ```
        '''
        errors = super().validate_playlist(playlist)
        sections = playlist.section_set.all()
        if sections.count() != 3:
            errors.append('There should be three sections in the playlist')
        if sorted([s.tag for s in sections]) != ['a', 'b', 'c']:
            errors.append('The sections should have the tags a, b, c')
        return errors

    def get_intro_explainer(self):
        return Explainer(
            instruction="Relatief Gehoor",
            steps=[
                Step("In dit experiment kun je testen hoe goed jouw relatieve gehoor is! Relatief gehoor is het vermogen om een melodie te herkennen, ongeacht of deze nu wat hoger of lager in toonhoogte wordt afgespeeld."),
                # Empty step adds some spacing between steps to improve readability
                Step(""),
                Step(
                    "Je krijgt twee melodieën te horen, verschillend in toonhoogte.", number=1),
                Step("Luister goed, want je kunt ze maar één keer afspelen!", number=2),
                Step("Aan jou de taak om te ontrafelen of deze melodieën hetzelfde zijn, ongeacht de toonhoogte! ", number=3),
            ],
            button_label="Start"
        )

    def next_round(self, session: Session):
        """Get action data for the next round"""

        rounds_passed = session.get_rounds_passed()

        # Round 1
        if rounds_passed == 0:
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return [self.get_intro_explainer(), *self.get_round(rounds_passed, session)]

        # Round 2
        if rounds_passed == 1:
            return [*self.get_score(session), *self.get_round(round, session)]

        # Final
        return self.get_final_round(session)

    def get_score(self, session):
        # Feedback
        last_result = session.last_result()

        if not last_result:
            logger.error("No last result")
            feedback = "Er is een fout opgetreden"
        else:
            if last_result.score == self.SCORE_CORRECT:
                feedback = "Dat is correct! De melodieën in de muziekfragmenten zijn inderdaad verschillend."
            else:
                feedback = "Helaas! De melodieën in de muziekfragmenten zijn toch echt verschillend."

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback)
        return [score]

    def get_round(self, round: int, session: Session):

        # Config
        # -----------------
        # section 1 is always section 'a'
        try:
            section1 = session.playlist.get_section(
                filter_by={'tag': 'a'})
        except:
            raise Exception(
                "Error: could not find section1 for round {}".format(round))

        # Get correct tag for round 0 or 1
        tag = 'b' if round == 0 else 'c'
        try:
            section2 = session.playlist.get_section(
                filter_by={'tag': tag})
        except:
            raise Exception(
                "Error: could not find section2 for round {}".format(round))

        # Fragments A,B,C are all different, so answer is always NO
        expected_response = "NO"

        # Question
        key = 'same_melody'
        question = ChoiceQuestion(
            question="Zijn deze twee melodieën hetzelfde?",
            key=key,
            choices={
                "YES": "Ja",
                "NO": "Nee",
            },
            view='BUTTON_ARRAY',
            submits=True,
            style=[ColorScheme.BOOLEAN],
            result_id=prepare_result(
                key, session, section=section1, expected_response=expected_response
            ),
        )
        form = Form([question])

        # Player
        playback = Multiplayer(
            [section1, section2],
            play_once=True,
            labels=['A', 'B' if round == 0 else 'C'],
        )

        trial = Trial(
            playback=playback,
            feedback_form=form,
            title=self.TITLE
        )
        return [trial]

    def calculate_score(self, result, data):
        return self.SCORE_CORRECT if result.expected_response == result.given_response else self.SCORE_WRONG

    def get_final_round(self, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session)

        # Final
        final_text = "Goed gedaan, jouw relatief gehoor is uitstekend!" if session.final_score >= 2 * \
            self.SCORE_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment6.html'))
        info = Info(
            body=body,
            heading="Relatief gehoor",
            button_label="Terug naar ToontjeHoger",
            button_link=get_current_experiment_url(session)
        )

        return [*score, final, info]
