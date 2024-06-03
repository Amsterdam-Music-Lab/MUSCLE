import logging
from django.template.loader import render_to_string

from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Trial, Explainer, Step, Score, Final, Playlist, Info, HTML
from experiment.actions.form import ButtonArrayQuestion, ChoiceQuestion, Form
from experiment.actions.playback import ImagePlayer
from experiment.actions.styles import STYLE_NEUTRAL
from .base import Base
from os.path import join
from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHogerKids2Preverbal(Base):
    ID = 'TOONTJE_HOGER_KIDS_2_PREVERBAL'
    TITLE = ""
    SCORE_CORRECT = 50
    SCORE_WRONG = 0

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Het eerste luisteren",
            steps=[
                Step(
                    "Je krijgt straks plaatjes te zien, een soort grafieken van een geluid. In een filmpje zie je zo een korte uitleg."),
                Step(
                    "Welk plaatje denk jij dat er hoort bij de stem van een mens?"),
                Step(
                    "Daarna volgt een vraag over twee baby huiltjes, kun jij het verschil horen?"),
            ],
            step_numbers=True,
            button_label="Start"
        )

        # 2 Spectrogram information
        spectrogram_info = self.get_spectrogram_info()

        # 3. Choose playlist.
        playlist = Playlist(experiment.playlists.all())

        return [
            explainer,
            spectrogram_info,
            playlist,
        ]

    def get_spectrogram_info(self):
        image_url = "/images/experiments/toontjehoger/spectrogram_info_nl.webp"
        description = "Dit is een spectogram. Wil je weten hoe dat werkt? Kijk dan het filmpje!"
        video = 'https://youtu.be/Mw5u3fe9aMI'
        body = f'<div class="center"><img src="{image_url}"></div><p>{description}</p><iframe width="560" src={video}></iframe>'

        # Return answer info view
        info = Info(
            body=body,
            heading="Wat is een spectrogram?",
            button_label="Volgende",
        )
        return info
    
    def next_round(self, session):
        """Get action data for the next round"""

        rounds_passed = session.rounds_passed()

        # Round 1
        if rounds_passed == 0:
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return self.get_round1(session)

        # Round 2
        if rounds_passed == 1:
            return [*self.get_score(session, rounds_passed), *self.get_round1_playback(session), *self.get_round2(round, session)]

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
                appendix = "Op het volgende scherm kun je de drie geluiden beluisteren."
                if last_result.score == self.SCORE_CORRECT:
                    feedback = "Goedzo! Op plaatje C zie je inderdaad de stem van een mens. " + appendix
                else:
                    feedback = "Helaas! Je antwoord was onjuist. Op plaatje C zag je de stem van een mens. " + appendix
            elif rounds_passed == 2:
                if last_result.score == self.SCORE_CORRECT:
                    feedback = "Goedzo! Geluid A is inderdaad de Franse baby."
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
            question="Welk plaatje denk jij dat er hoort bij de stem van een mens?",
            key=key,
            choices={
                'A': 'A',
                'B': 'B',
                'C': 'C',
            },
            view='BUTTON_ARRAY',
            submits=True,
            result_id=prepare_result(
                key, session, expected_response="C"
            )
        )
        form = Form([question])

        image_trial = Trial(
            html=HTML(
            body='<img src="{}" style="height:calc(100% - 260px);max-height:326px;max-width: 100%;"/>'.format(
                "/images/experiments/toontjehoger/preverbal_1.webp")),
            feedback_form=form,
            title=self.TITLE,
        )

        return [image_trial]
    
    def get_round1_playback(self, session):
        # Get sections
        sectionA = session.section_from_any_song(
            filter_by={'tag': 'a', 'group': '1'})
        if not sectionA:
            raise Exception(
                "Error: could not find section A for round 1")

        sectionB = session.section_from_any_song(
            filter_by={'tag': 'b', 'group': '1'})
        if not sectionB:
            raise Exception(
                "Error: could not find section B for round 1")

        sectionC = session.section_from_any_song(
            filter_by={'tag': 'c', 'group': '1'})
        if not sectionB:
            raise Exception(
                "Error: could not find section C for round 1")

        # Player
        playback = ImagePlayer(
            [sectionA, sectionB, sectionC],
            label_style='ALPHABETIC',
            images=["/images/experiments/toontjehoger/spectrogram-trumpet.webp", "/images/experiments/toontjehoger/spectrogram-whale.webp", "/images/experiments/toontjehoger/spectrogram-human.webp"],
            image_labels = ['Trompet', 'Walvis', 'Mens']
        )

        trial = Trial(
            playback=playback,
            feedback_form=None,
            title=self.TITLE,
            style='primary-form'
        )
        return [trial]
    
    def get_round2(self, round, session):

        # Get sections
        # French
        sectionA = session.section_from_any_song(
            filter_by={'tag': 'a', 'group': '2'})
        if not sectionA:
            raise Exception(
                "Error: could not find section A for round 2")
        # German
        sectionB = session.section_from_any_song(
            filter_by={'tag': 'b', 'group': '2'})
        if not sectionB:
            raise Exception(
                "Error: could not find section B for round 2")

        # Player
        playback = ImagePlayer(
            [sectionA, sectionB],
            label_style='ALPHABETIC',
            images=["/images/experiments/toontjehoger/spectrogram-baby-french.webp", "/images/experiments/toontjehoger/spectrogram-baby-german.webp"],
        )

        # Question
        key = 'baby'
        question = ChoiceQuestion(
            question="Hierboven zie je twee spectogrammen van baby huiltjes.  Een van een Duitse baby en een van een Franse baby. De talen Frans en Duits klinken heel anders. Kun jij bedenken welke van deze baby’s de Franse baby is?",
            key=key,
            choices={
                "A": "A",
                "B": "B",
            },
            view='BUTTON_ARRAY',
            submits=True,
            result_id=prepare_result(key, session, expected_response="A"),
            style=STYLE_NEUTRAL
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
        score = self.get_score(session, session.rounds_passed())

        # Final
        final_text = "Goed gedaan!" if session.final_score >= 2 * \
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
            button_link="/toontjehoger"
        )

        return [*score, final, info]
