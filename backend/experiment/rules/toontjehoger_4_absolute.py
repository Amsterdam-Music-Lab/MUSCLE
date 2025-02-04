import re
import logging
import random
from os.path import join
from django.template.loader import render_to_string
from section.models import Playlist
from experiment.utils import non_breaking_spaces
from .toontjehoger_1_mozart import toontjehoger_ranks
from experiment.actions import Trial, Explainer, Step, Score, Final, Info
from experiment.actions.form import ButtonArrayQuestion, Form
from experiment.actions.playback import Multiplayer
from experiment.actions.styles import ColorScheme
from experiment.actions.utils import get_current_experiment_url
from experiment.utils import create_player_labels
from .base import BaseRules
from result.utils import prepare_result
from session.models import Session

logger = logging.getLogger(__name__)


class ToontjeHoger4Absolute(BaseRules):
    ID = 'TOONTJE_HOGER_4_ABSOLUTE'
    TITLE = ""
    SCORE_CORRECT = 20
    SCORE_WRONG = 0
    # number of songs (each with a,b,c version) in the playlist
    PLAYLIST_ITEMS = 13

    def get_intro_explainer(self):
        return Explainer(
            instruction="Absoluut gehoor",
            steps=[
                Step(
                    "Je gaat zo luisteren naar fragmenten muziek die je misschien herkent als de intro van een tv-programma of serie."),
                Step(
                    "Van ieder fragment kan je twee versies luisteren. Eén hiervan is het origineel. De andere hebben we een beetje hoger of lager gemaakt."),
                Step("Kan jij horen welke van de twee versies precies zo hoog of laag is als je 'm kent? Welke is het origineel?"),
            ],
            step_numbers=True,
            button_label="Start"
        )

    def next_round(self, session):
        """Get action data for the next round"""

        rounds_passed = session.get_rounds_passed()

        # Round 1
        if rounds_passed == 0:
            return [self.get_intro_explainer(), *self.get_round(session)]

        # Round 2 - 4
        if rounds_passed < session.block.rounds:
            return [*self.get_score(session), *self.get_round(session)]

        # Final
        return self.get_final_round(session)

    def get_trial_question(self):
        return "Welk fragment heeft de juiste toonhoogte?"

    def get_round(self, session: Session):
        # Get available section groups
        results = session.result_set.all()
        available_groups = list(map(str, range(1, self.PLAYLIST_ITEMS)))
        for result in results:
            available_groups.remove(result.section.group)

        # Get sections

        # Original (A)
        section1 = session.playlist.get_section(
            filter_by={'tag': 'a', 'group__in': available_groups})
        if not section1:
            raise Exception(
                "Error: could not find section 1")

        # Changed (B/C)
        variant = random.choice(["b", "c"])
        section2 = session.playlist.get_section(
            filter_by={'tag': variant, 'group': section1.group})
        if not section2:
            raise Exception(
                "Error: could not find section 2")

        # Random section order
        sections = [section1, section2]
        random.shuffle(sections)

        # Player
        playback = Multiplayer(
            sections,
            labels=create_player_labels(len(sections), 'alphabetic'),
            style=[ColorScheme.NEUTRAL_INVERTED],
        )

        # Question
        key = 'pitch'
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
                section=section1,
                expected_response="A" if sections[0].id == section1.id else "B",
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

            feedback += " Je luisterde naar de intro van {}.".format(
                non_breaking_spaces(last_result.section.song.name))

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
        if session.final_score >= session.block.rounds * 0.8 * self.SCORE_CORRECT:
            final_text = "Goed gedaan! Jouw absolute gehoor is uitstekend!"
        elif session.final_score >= session.block.rounds * 0.5 * self.SCORE_CORRECT:
            final_text = "Goed gedaan! Jouw absolute gehoor is best OK!"

        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        body = render_to_string(
            join('info', 'toontjehoger', 'experiment4.html'))
        info = Info(
            body=body,
            heading="Absoluut gehoor",
            button_label="Terug naar ToontjeHoger",
            button_link=get_current_experiment_url(session)
        )

        return [*score, final, info]

    def validate_playlist_groups(self, groups):
        integer_groups = []
        integer_pattern = re.compile(r'^-?\d+$')
        for group in groups:
            if not integer_pattern.match(str(group)):
                return ["Groups in playlist sections should be numbers. This playlist has groups: {}".format(groups)]

            integer_groups.append(int(group))

        # Check if the groups are sequential and unique
        integer_groups.sort()
        if integer_groups != list(range(1, len(groups) + 1)):
            return ['Groups in playlist sections should be sequential numbers starting from 1 to the number of items in the playlist ({}). E.g. "1, 2, 3, ... {}"'.format(self.PLAYLIST_ITEMS, self.PLAYLIST_ITEMS)]

        return []

    def validate_playlist(self, playlist: Playlist):
        errors = super().validate_playlist(playlist)

        # Get group values from sections, ordered by group
        groups = list(playlist.section_set.values_list(
            'group', flat=True).distinct())

        # Check if the groups are sequential and unique
        errors += self.validate_playlist_groups(groups)

        # Check if the tags are 'a', 'b' or 'c'
        tags = list(
            playlist.section_set
            .values_list('tag', flat=True)
            .distinct()
            .order_by('tag')
        )

        if tags != ['a', 'b', 'c']:
            errors.append("Tags in playlist sections should be 'a', 'b' or 'c'. This playlist has tags: {}".format(tags))

        return errors
