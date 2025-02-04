import re
import logging
import random
from os.path import join
from django.template.loader import render_to_string
from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Trial, Explainer, Step, Score, Final, Info
from experiment.actions.form import ButtonArrayQuestion, Form
from experiment.actions.playback import Multiplayer
from experiment.actions.styles import ColorScheme
from experiment.actions.utils import get_current_experiment_url
from section.models import Playlist
from session.models import Session
from .base import BaseRules
from experiment.utils import create_player_labels, non_breaking_spaces

from result.utils import prepare_result

logger = logging.getLogger(__name__)


class ToontjeHoger5Tempo(BaseRules):
    ID = "TOONTJE_HOGER_5_TEMPO"
    TITLE = ""
    SCORE_CORRECT = 20
    SCORE_WRONG = 0

    def get_intro_explainer(self):
        return Explainer(
            instruction="Timing en tempo",
            steps=[
                Step("Je krijgt dadelijk twee verschillende uitvoeringen van hetzelfde stuk te horen."),
                Step(
                    "Eén wordt op de originele snelheid (tempo) afgespeeld, terwijl de ander iets is versneld of vertraagd."
                ),
                Step("Kan jij horen welke het origineel is?"),
                Step("Let hierbij vooral op de timing van de muzikanten."),
            ],
            step_numbers=True,
            button_label="Start",
        )

    def next_round(self, session):
        """Get action data for the next round"""

        rounds_passed = session.get_rounds_passed()

        # Round 1
        if rounds_passed == 0:
            # No combine_actions because of inconsistent next_round array wrapping in first round
            return [self.get_intro_explainer(), *self.get_round(session, rounds_passed)]

        # Round 2
        if rounds_passed < session.block.rounds:
            return [*self.get_score(session), *self.get_round(session, rounds_passed)]

        # Final
        return self.get_final_round(session)

    def get_random_section_pair(self, session: Session, genre: str):
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
        previous_tags = [result.section.tag for result in session.result_set.all()]

        # Get a random, unused track
        # Loop until there is a valid tag
        iterations = 0
        valid_tag = False
        tag_base = ""
        tag_original = ""
        while not valid_tag:
            track = random.choice([1, 2, 3, 4, 5])
            pair = random.choice([1, 2])
            tag_base = "{}{}_P{}_".format(
                genre.upper(),
                track,
                pair,
            )
            tag_original = tag_base + "OR"
            if tag_original not in previous_tags:
                valid_tag = True

            # Failsafe: prevent infinite loop
            # If this happens, just reuse a track
            iterations += 1
            if iterations > 10:
                valid_tag = True

        tag_changed = tag_base + "CH"

        section_original = session.playlist.get_section(filter_by={"tag": tag_original, "group": "or"})

        if not section_original:
            raise Exception("Error: could not find original section: {}".format(tag_original))

        section_changed = self.get_section_changed(session=session, tag=tag_changed)

        sections = [section_original, section_changed]
        random.shuffle(sections)
        return sections

    def get_section_changed(self, session, tag):
        try:
            section_changed = session.playlist.get_section(filter_by={"tag": tag, "group": "ch"})
        except:
            raise Exception("Error: could not find changed section: {}".format(tag))
        return section_changed

    def get_trial_question(self):
        return "Welk fragment wordt in het originele tempo afgespeeld?"

    def get_round(self, session, round):
        # Get sections
        genre = ["C", "J", "R"][round % 3]

        sections = self.get_random_section_pair(session, genre)
        section_original = sections[0] if sections[0].group == "or" else sections[1]

        # Player
        playback = Multiplayer(
            sections,
            labels=create_player_labels(len(sections), "alphabetic"),
            style=[ColorScheme.NEUTRAL_INVERTED],
        )

        # Question
        key = "pitch"
        question = ButtonArrayQuestion(
            question=self.get_trial_question(),
            key=key,
            choices={
                "A": "A",
                "B": "B",
            },
            submits=True,
            result_id=prepare_result(
                key,
                session,
                section=section_original,
                expected_response="A" if sections[0].id == section_original.id else "B",
            ),
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

    def get_section_pair_from_result(self, result):
        section_original = result.section

        if section_original is None:
            raise Exception("Error: could not get section from result")

        tag_changed = section_original.tag.replace("OR", "CH")
        section_changed = self.get_section_changed(session=result.session, tag=tag_changed)

        if section_changed is None:
            raise Exception("Error: could not get changed section for tag: {}".format(tag_changed))

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
                feedback = "Goedzo! Het was inderdaad antwoord {}!".format(last_result.expected_response.upper())
            else:
                feedback = "Helaas! Het juiste antwoord was {}.".format(last_result.expected_response.upper())

            section_original, section_changed = self.get_section_pair_from_result(last_result)

            # Create feedback message
            # - Track names are always the same
            # - Artist could be different
            if section_original.artist_name() == section_changed.artist_name():
                feedback += " Je hoorde {}, in beide fragmenten uitgevoerd door {}.".format(
                    last_result.section.song_name(),
                    last_result.section.artist_name(),
                )
            else:
                section_a = section_original if last_result.expected_response == "A" else section_changed
                section_b = section_changed if section_a.id == section_original.id else section_original
                feedback += " Je hoorde {} uitgevoerd door A) {} en B) {}.".format(
                    section_a.song_name(),
                    non_breaking_spaces(section_a.artist_name()),
                    non_breaking_spaces(section_b.artist_name()),
                )

        # Return score view
        config = {"show_total_score": True}
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
        if session.final_score >= session.block.rounds * 0.8 * self.SCORE_CORRECT:
            final_text = "Goed gedaan! Jouw timing is uitstekend!"
        elif session.final_score >= session.block.rounds * 0.5 * self.SCORE_CORRECT:
            final_text = "Goed gedaan! Jouw timing is best OK!"

        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={"text": "Wat hebben we getest?"},
        )

        # Info page
        body = render_to_string(join("info", "toontjehoger", "experiment5.html"))
        info = Info(
            body=body,
            heading="Timing en tempo",
            button_label="Terug naar ToontjeHoger",
            button_link=get_current_experiment_url(session),
        )

        return [*score, final, info]

    def validate_tags(self, tags):
        errors = []
        erroneous_tags = []

        for tag in tags:
            if not re.match(r"^[CJR][1-5]_P[12]_(OR|CH)$", tag):
                erroneous_tags.append(tag)

        if erroneous_tags:
            errors.append(
                "Tags should start with either 'C', 'J' or 'R', followed by a number between 1 and 5, "
                "followed by '_P', followed by either 1 or 2, followed by either '_OR' or '_CH'. "
                "Invalid tags: {}".format(", ".join(erroneous_tags))
            )

        return errors

    def validate_playlist(self, playlist: Playlist):
        errors = super().validate_playlist(playlist)
        sections = playlist.section_set.all()
        groups = sorted(list(set([section.group for section in sections])))

        if groups != ["ch", "or"]:
            errors.append("The playlist must contain two groups: 'or' and 'ch'. Found: {}".format(groups))

        tags = sorted(list(set([section.tag for section in sections])))

        # Check if all tags are valid
        errors += self.validate_tags(tags)

        return errors
