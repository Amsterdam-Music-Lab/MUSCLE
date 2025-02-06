import logging
from os.path import join

from django.template.loader import render_to_string

from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Trial, Explainer, Step, Score, Final, Playlist, Info, HTML
from experiment.actions.form import ButtonArrayQuestion, ChoiceQuestion, Form
from experiment.actions.playback import ImagePlayer
from experiment.actions.styles import ColorScheme
from experiment.actions.utils import get_current_experiment_url
from experiment.utils import create_player_labels
from .base import BaseRules
from result.utils import prepare_result
from section.models import Playlist

logger = logging.getLogger(__name__)


class ToontjeHoger2Preverbal(BaseRules):
    ID = 'TOONTJE_HOGER_2_PREVERBAL'
    TITLE = ""
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    def validate_playlist(self, playlist: Playlist):
        ''' This is the original ToontjeHoger2Preverbal playlist:
        ```
        AML,Duitse baby,0.0,1.0,/toontjehoger/preverbal/4_duitse_baby.mp3,b,2
        AML,Franse baby,0.0,1.0,/toontjehoger/preverbal/5_franse_baby.mp3,a,2
        AML,Mens,0.0,1.0,/toontjehoger/preverbal/1_mens.mp3,c,1
        AML,Trompet,0.0,1.0,/toontjehoger/preverbal/3_trompet.mp3,a,1
        AML,Walvis,0.0,1.0,/toontjehoger/preverbal/2_walvis.mp3,b,1
        ```
        '''
        sections = playlist.section_set.all()
        errors = []
        if len(sections) != 5:
            errors.append('The playlist should contain exactly 5 sections')

        first_round_sections = sections.filter(group='1')
        if first_round_sections.count() != 3:
            errors.append(
                'There should be 3 sections with group 1 (first round)')
        if sorted(first_round_sections.values_list('tag', flat=True).distinct()) != ['a', 'b', 'c']:
            errors.append(
                'The first round sections should have tags a, b, c'
            )

        second_round_sections = sections.filter(group='2')
        if second_round_sections.count() != 2:
            errors.append(
                'There should be 2 sections with group 2 (second round)')
        if sorted(second_round_sections.values_list('tag', flat=True).distinct()) != ['a', 'b']:
            errors.append(
                'The second round sections should have tags a, b'
            )

        return errors

    def get_intro_explainer(self):
        return Explainer(
            instruction="Het eerste luisteren",
            steps=[
                Step(
                    "Je krijgt drie spectrogrammen te zien met de vraag: welk geluid is van een mens?"
                ),
                Step(
                    "Daarvoor eerst nog wat uitleg van wat een spectrogram is, natuurlijk."
                ),
                Step(
                    "Tenslotte krijg je twee geluiden te horen met de vraag: welke baby is in Frankrijk geboren?"
                ),
            ],
            step_numbers=True,
            button_label="Start",
        )

    def get_spectrogram_info(self):
        image_url = "/images/experiments/toontjehoger/spectrogram_info_nl.webp"
        description = "Een spectrogram is een visuele weergave van geluid, waarin je kan zien hoe een geluid verandert over de tijd. Hoe witter, hoe meer energie op die frequentie."
        body = '<div class="center"><img src="{}"></div><p>{}</p>'.format(
            image_url, description)

        # Return answer info view
        info = Info(
            body=body,
            heading="Wat is een spectrogram?",
            button_label="Volgende",
        )
        return info

    def next_round(self, session):
        """Get action data for the next round"""

        rounds_passed = session.get_rounds_passed()

        # Round 1
        if rounds_passed == 0:
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return [
                self.get_intro_explainer(),
                self.get_spectrogram_info(),
                self.get_round1(session),
            ]

        # Round 2
        if rounds_passed == 1:
            return [
                *self.get_score(session, rounds_passed),
                *self.get_round1_playback(session),
                *self.get_round2(round, session),
            ]

        # Final
        return self.get_final_round(session)

    def get_score(self, session, rounds_passed):
        # Feedback
        last_result = session.last_result()
        feedback = ""
        if not last_result:
            logger.error("No last result")
            feedback = "Er is een fout opgetreden"
        else:
            if rounds_passed == 1:
                appendix = "Op het volgende scherm kun je de geluiden beluisteren."
                if last_result.score == self.SCORE_CORRECT:
                    feedback = "Dat is correct! Spectrogram C is inderdaad van een mens. " + appendix
                else:
                    feedback = "Helaas! Je antwoord was onjuist. Het geluid van spectrogram C is van een mens. " + appendix
            elif rounds_passed == 2:
                if last_result.score == self.SCORE_CORRECT:
                    feedback = "Dat is correct! Geluid A is inderdaad de Franse baby."
                else:
                    feedback = "Helaas! Geluid A is de Franse baby."

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback)
        return [score]

    def get_round1(self, session):
        # Question
        key = 'expected_spectrogram'
        question = ButtonArrayQuestion(
            question=self.get_round1_question(),
            key=key,
            choices={
                'A': 'A',
                'B': 'B',
                'C': 'C',
            },
            view='BUTTON_ARRAY',
            submits=True,
            result_id=prepare_result(key, session, expected_response="C"),
            style=[ColorScheme.NEUTRAL_INVERTED],
        )
        form = Form([question])

        image_trial = Trial(
            html=HTML(
                body='<img src="{}" style="max-height:326px;max-width: 100%;"/>'.format(
                    "/images/experiments/toontjehoger/preverbal_1.webp"
                )
            ),
            feedback_form=form,
            title=self.TITLE,
        )

        return image_trial

    def get_round1_question(self):
        return "Welk spectrogram toont het geluid van een mens?"

    def get_round_2_question(self):
        return "Welke baby is in Frankrijk geboren?"

    def get_round1_playback(self, session):
        # Get sections
        sectionA = session.playlist.get_section(
            filter_by={'tag': 'a', 'group': '1'})
        if not sectionA:
            raise Exception(
                "Error: could not find section A for round 1")

        sectionB = session.playlist.get_section(
            filter_by={'tag': 'b', 'group': '1'})
        if not sectionB:
            raise Exception(
                "Error: could not find section B for round 1")

        sectionC = session.playlist.get_section(
            filter_by={'tag': 'c', 'group': '1'})
        if not sectionB:
            raise Exception(
                "Error: could not find section C for round 1")

        # Player
        sections = [sectionA, sectionB, sectionC]
        playback = ImagePlayer(
            sections,
            labels=create_player_labels(len(sections), 'alphabetic'),
            images=[
                "/images/experiments/toontjehoger/spectrogram-trumpet.webp",
                "/images/experiments/toontjehoger/spectrogram-whale.webp",
                "/images/experiments/toontjehoger/spectrogram-human.webp",
            ],
            image_labels=['Trompet', 'Walvis', 'Mens'],
            style=[ColorScheme.NEUTRAL_INVERTED],
        )

        trial = Trial(
            playback=playback,
            feedback_form=None,
            title=self.TITLE
        )
        return [trial]

    def get_round2(self, round, session):

        # Get sections
        # French
        sectionA = session.playlist.get_section(
            filter_by={'tag': 'a', 'group': '2'})
        if not sectionA:
            raise Exception(
                "Error: could not find section A for round 2")
        # German
        sectionB = session.playlist.get_section(
            filter_by={'tag': 'b', 'group': '2'})
        if not sectionB:
            raise Exception(
                "Error: could not find section B for round 2")

        # Player
        sections = [sectionA, sectionB]
        playback = ImagePlayer(
            sections,
            labels=create_player_labels(len(sections), 'alphabetic'),
            images=[
                "/images/experiments/toontjehoger/spectrogram-baby-french.webp",
                "/images/experiments/toontjehoger/spectrogram-baby-german.webp",
            ],
            style=[ColorScheme.NEUTRAL_INVERTED],
        )

        # Question
        key = 'baby'
        question = ChoiceQuestion(
            question=self.get_round_2_question(),
            key=key,
            choices={
                "A": "A",
                "B": "B",
            },
            view='BUTTON_ARRAY',
            submits=True,
            result_id=prepare_result(key, session, expected_response="A"),
            style=[ColorScheme.NEUTRAL_INVERTED],
        )
        form = Form([question])

        trial = Trial(
            playback=playback,
            feedback_form=form,
            title=self.TITLE,
        )
        return [trial]

    def calculate_score(self, result, data):
        return self.SCORE_CORRECT if result.expected_response == result.given_response else self.SCORE_WRONG

    def get_final_round(self, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session, session.get_rounds_passed())

        # Final
        final_text = "Goed gedaan! Je hebt beide vragen correct beantwoord!" if session.final_score >= 2 * \
            self.SCORE_CORRECT else "Dat bleek toch even lastig!"
        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment2.html'))
        info = Info(
            body=body,
            heading="Het eerste luisteren",
            button_label="Terug naar ToontjeHoger",
            button_link=get_current_experiment_url(session)
        )

        return [*score, final, info]
