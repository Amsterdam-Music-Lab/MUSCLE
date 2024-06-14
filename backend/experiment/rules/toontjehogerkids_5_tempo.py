import logging
import random
from os.path import join
from django.template.loader import render_to_string
from .toontjehoger_1_mozart import toontjehoger_ranks
from .toontjehoger_5_tempo import ToontjeHoger5Tempo
from experiment.actions import Explainer, Step, Score, Final, Info
from experiment.utils import non_breaking_spaces

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
                    "Je krijgt zo steeds twee keer een stukje muziek te horen met piepjes erin."),
                Step(
                    "Bij de ene versie zijn de piepjes in de maat, bij de andere niet in de maat.   "),
                Step(
                    "Kan jij horen waar de piepjes in de maat van de muziek zijn?"),
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
          - genre: unused

          return a section from an unused song, in both its original and changed variant
        """

        section_original = session.section_from_unused_song(
            filter_by={'group': "or"})

        if not section_original:
            raise Exception(
                "Error: could not find original section: {}".format(section_original))

        section_changed = self.get_section_changed(
            session=session, song=section_original.song)

        sections = [section_original, section_changed]
        random.shuffle(sections)
        return sections

    def get_section_changed(self, session, song):
        section_changed = session.playlist.section_set.get(
            song__name=song.name, song__artist=song.artist, group='ch'
        )
        if not section_changed:
            raise Exception(
                "Error: could not find changed section: {}".format(song))
        return section_changed

    def get_trial_question(self):
        return "Kan jij horen waar de piepjes in de maat van de muziek zijn?"

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

            # Create feedback message
            # - Track names are always the same
            feedback += " Je hoorde '{}' van {}.".format(
                last_result.section.song.name, last_result.section.song.artist)

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
        final_text = "Best lastig!"
        if session.final_score >= session.experiment.rounds * 0.5 * self.SCORE_CORRECT:
            final_text = "Goed gedaan!"

        final = Final(
            session=session,
            final_text=final_text,
            rank=toontjehoger_ranks(session),
            button={'text': 'Wat hebben we getest?'}
        )

        # Info page
        debrief_message = "Dit is een test die maatgevoel meet. Onderzoekers hebben laten zien dat de meeste mensen goed maatgevoel hebben. Maar als je nou niet zo goed kan dansen, heb jij dan toch niet zo'n goed maatgevoel? En kan je dit leren? Bekijk de filmpjes voor het antwoord!"
        body = render_to_string(
            join('info', 'toontjehogerkids', 'debrief.html'),
            {'debrief': debrief_message,
            #  'vid1': 'https://www.youtube.com/embed/lsQx-mJ4-cA?si=BuO5FO56I4rThTAY?rel=0',
            #  'vid2': 'https://www.youtube.com/embed/9LSmfsiEXhI?si=WsxrYN3UnHiiG8qT?rel=0'})
            # use youtube-nocookie
                'vid1': 'https://www.youtube-nocookie.com/embed/lsQx-mJ4-cA?si=BuO5FO56I4rThTAY?rel=0&amp;showinfo=0',
                'vid2': 'https://www.youtube-nocookie.com/embed/9LSmfsiEXhI?si=WsxrYN3UnHiiG8qT?rel=0&amp;showinfo=0'})
        info = Info(
            body=body,
            heading="Timing en tempo",
            button_label="Terug naar ToontjeHogerKids",
            button_link="/collection/thkids"
        )

        return [*score, final, info]

    def validate_tags(self, tags):
        # No validation needed for TH5 Kids
        return []
