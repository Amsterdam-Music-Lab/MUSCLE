import logging
import random
from os.path import join
from django.template.loader import render_to_string
from .toontjehoger_1_mozart import toontjehoger_ranks
from .toontjehoger_5_tempo import ToontjeHoger5Tempo
from experiment.actions import Explainer, Step, Score, Final, Info
from experiment.utils import non_breaking_spaces

from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHogerKids5Tempo(ToontjeHoger5Tempo):
    ID = 'TOONTJE_HOGER_KIDS_5_TEMPO'

    def first_round(self, experiment):
        """Create data for the first experiment rounds."""

        # 1. Explain game.
        explainer = Explainer(
            instruction="Maatgevoel",
            steps=[
                Step(
                    "Je krijgt zo twee stukjes muziek te horen, de muziek is 2x hetzelfde."),
                Step("Bij die muziek hoor je ook klikjes: die passen de ene keer goed bij de maat van de muziek, terwijl ze de andere keer niet goed gelijk lopen.   "),
                Step(
                    "Kan jij horen waar de klikjes goed bij de maat van de muziek passen?"),
            ],
            step_numbers=True,
            button_label="Start"
        )

        return [
            explainer
        ]

    def get_random_section_pair(self, session, genre):
        """
          - session: current Session
          - genre: (C)lassic (J)azz (R)ock

          Voor de track: genereer drie random integers van 1-5 (bijv. [4 2 4])
          Plak deze aan de letters C, J en R (bijv. [C4, J2, R4])
          Voor het paar: genereer drie random integers van 1-2 (bijv. [1 2 2])
          Plak deze aan de letter P (bijv. P1, P2, P2)
          We willen zowel de originele als de veranderde versie van het paar. Dus combineer
          bovenstaande met OR en CH (bijv. “C4_P1_OR”, “C4_P1_CH”, etc.)
        """
        # Previous tags
        previous_tags = [
            result.section.tag for result in session.result_set.all()]

        # Get a random, unused track
        # Loop until there is a valid tag
        iterations = 0
        valid_tag = False
        tag_base = ""
        tag_original = ""
        while(not valid_tag):
            track = random.choice([1, 2, 3, 4, 5])
            pair = random.choice([1, 2])
            tag_base = "{}{}_P{}_".format(genre.upper(), track, pair, )
            tag_original = tag_base + "OR"
            if not (tag_original in previous_tags):
                valid_tag = True

            # Failsafe: prevent infinite loop
            # If this happens, just reuse a track
            iterations += 1
            if iterations > 10:
                valid_tag = True

        tag_changed = tag_base + "CH"

        section_original = session.section_from_any_song(
            filter_by={'tag': tag_original, 'group': "or"})

        if not section_original:
            raise Exception(
                "Error: could not find original section: {}".format(tag_original))

        section_changed = self.get_section_changed(
            session=session, tag=tag_changed)

        sections = [section_original, section_changed]
        random.shuffle(sections)
        return sections
 
    def get_section_changed(self, session, tag):
        section_changed = session.section_from_any_song(
            filter_by={'tag': tag, 'group': "ch"})
        if not section_changed:
            raise Exception(
                "Error: could not find changed section: {}".format(tag))
        return section_changed

    def get_trial_question(self):
        return "Kan jij horen waar de klikjes goed bij de maat van de muziek passen?"
    
    def get_section_pair_from_result(self, result):
        section_original = result.section

        if section_original is None:
            raise Exception(
                "Error: could not get section from result")

        tag_changed = section_original.tag.replace("OR", "CH")
        section_changed = self.get_section_changed(
            session=result.session, tag=tag_changed)

        if section_changed is None:
            raise Exception(
                "Error: could not get changed section for tag: {}".format(
                    tag_changed))

        return (section_original, section_changed)

    def get_score(self, session):
        # Feedback
        last_result = session.last_result()
        feedback = ""
        if not last_result:
            logger.error("No last result")
            feedback = "Er is een fout opgetreden"
        else:
            if last_result.score == self.SCORE_CORRECT:
                feedback = "Goedzo! Het was inderdaad antwoord {}!".format(
                    last_result.expected_response.upper())
            else:
                feedback = "Helaas! Het juiste antwoord was {}.".format(
                    last_result.expected_response.upper())

            section_original, section_changed = self.get_section_pair_from_result(
                last_result)

            # Create feedback message
            # - Track names are always the same
            # - Artist could be different
            if section_original.song.artist == section_changed.song.artist:
                feedback += " Je hoorde {}, in beide fragmenten uitgevoerd door {}.".format(
                    last_result.section.song.name, last_result.section.song.artist)
            else:
                section_a = section_original if last_result.expected_response == "A" else section_changed
                section_b = section_changed if section_a.id == section_original.id else section_original
                feedback += " Je hoorde {} uitgevoerd door A) {} en B) {}.".format(
                    section_a.song.name, non_breaking_spaces(section_a.song.artist), non_breaking_spaces(section_b.song.artist))

        # Return score view
        config = {'show_total_score': True}
        score = Score(session, config=config, feedback=feedback)
        return [score]

    def get_final_round(self, session):

        # Finish session.
        session.finish()
        session.save()

        # Score
        score = self.get_score(session)

        # Final
        final_text = "Dat bleek toch even lastig!"
        if session.final_score >= session.experiment.rounds * 0.5 * self.SCORE_CORRECT:
            final_text = "Goed gedaan!"

        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        body = render_to_string(
            join('info', 'toontjehogerkids', 'experiment5.html'))
        info = Info(
            body=body,
            heading="Timing en tempo",
            button_label="Terug naar ToontjeHoger",
            button_link="/collection/thkids"
        )

        return [*score, final, info]
