import logging
import random

from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from experiment.actions import Explainer, Final, Playlist, Score, Step, Trial
from experiment.actions.form import BooleanQuestion, Form
from experiment.actions.playback import Autoplay
from experiment.actions.styles import ColorScheme, ButtonStyle
from experiment.actions.wrappers import song_sync
from question.questions import QUESTION_GROUPS
from result.utils import prepare_result
from section.models import Section
from session.models import Session


logger = logging.getLogger(__name__)


class Hooked(BaseRules):
    """Superclass for Hooked experiment rules"""

    ID = "HOOKED"
    default_consent_file = "consent/consent_hooked.html"
    recognition_time = 15  # response time for "Do you know this song?"
    sync_time = 15  # response time for "Did the track come back in the right place?"
    # if the track continues in the wrong place: minimal shift forward (in seconds)
    min_jitter = 10
    # if the track continutes in the wrong place: maximal shift forward (in seconds)
    max_jitter = 15
    heard_before_time = 15  # response time for "Have you heard this song in previous rounds?"
    question_offset = 5  # how many rounds will be presented without questions
    questions = True
    counted_result_keys = ["recognize", "heard_before"]
    play_method = "BUFFER"

    def __init__(self):
        self.question_series = [
            {
                "name": "DEMOGRAPHICS",
                "keys": QUESTION_GROUPS["DEMOGRAPHICS"],
                "randomize": True,
            },  # 1. Demographic questions (7 questions)
            {"name": "MSI_OTHER", "keys": ["msi_39_best_instrument"], "randomize": False},
            {
                "name": "MSI_FG_GENERAL",
                "keys": QUESTION_GROUPS["MSI_FG_GENERAL"],
                "randomize": True,
            },  # 2. General music sophistication
            {
                "name": "MSI_ALL",
                "keys": QUESTION_GROUPS["MSI_ALL"],
                "randomize": True,
            },  # 3. Complete music sophistication (20 questions)
            {"name": "STOMP20", "keys": QUESTION_GROUPS["STOMP20"], "randomize": True},  # 4. STOMP (20 questions)
            {"name": "TIPI", "keys": QUESTION_GROUPS["TIPI"], "randomize": True},  # 5. TIPI (10 questions)
        ]

    def get_intro_explainer(self):
        """Explain the game"""
        return Explainer(
            instruction="How to Play",
            steps=[
                Step(
                    _(
                        "Do you recognise the song? Try to sing along. The faster you recognise songs, the more points you can earn."
                    )
                ),
                Step(
                    _(
                        "Do you really know the song? Keep singing or imagining the music while the sound is muted. The music is still playing: you just can’t hear it!"
                    )
                ),
                Step(
                    _(
                        "Was the music in the right place when the sound came back? Or did we jump to a different spot during the silence?"
                    )
                ),
            ],
            step_numbers=True,
            button_label=_("Let's go!"),
        )

    def next_round(self, session: Session):
        """Get action data for the next round"""
        round_number = session.get_rounds_passed(self.counted_result_keys)

        # If the number of results equals the number of block.rounds,
        # close the session and return data for the final_score view.
        if round_number == session.block.rounds:
            # Finish session.
            session.finish()
            session.save()

            # Return a score and final score action.
            total_score = session.total_score()
            return [
                self.get_score(session, round_number),
                Final(
                    session=session,
                    final_text=self.final_score_message(session),
                    rank=self.rank(session),
                    show_profile_link=True,
                    button={
                        "text": _("Play again"),
                        "link": self.get_play_again_url(session),
                    },
                ),
            ]

        # Get next round number and initialise actions list. Two thirds of
        # rounds will be song_sync; the remainder heard_before.

        # Collect actions.
        actions = []

        if round_number == 0:
            # Intro explainer
            actions.append(self.get_intro_explainer())
            # Choose playlist
            actions.append(Playlist(session.block.playlists.all()))

            # Plan sections
            self.plan_sections(session)
            # Go to SongSync straight away.
            actions.extend(self.next_song_sync_action(session, round_number))
        else:
            # Create a score action.
            actions.append(self.get_score(session, round_number))
            heard_before_offset = session.json_data.get("heard_before_offset")

            # SongSync rounds. Skip questions until round indicated by question_offset.
            if round_number in range(1, self.question_offset):
                actions.extend(self.next_song_sync_action(session, round_number))
            elif round_number in range(self.question_offset, heard_before_offset):
                question_trial = self.get_single_question(session)
                if question_trial:
                    actions.append(question_trial)
                actions.extend(self.next_song_sync_action(session, round_number))

            # HeardBefore rounds
            elif round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(self.heard_before_explainer())
                actions.append(self.next_heard_before_action(session, round_number))
            elif round_number > heard_before_offset:
                question_trial = self.get_single_question(session)
                if question_trial:
                    actions.append(question_trial)
                actions.append(self.next_heard_before_action(session, round_number))

        return actions

    def heard_before_explainer(self):
        """Explainer for heard-before rounds"""
        return Explainer(
            instruction=_("Bonus Rounds"),
            steps=[
                Step(_("Listen carefully to the music.")),
                Step(_("Did you hear the same song during previous rounds?")),
            ],
            step_numbers=True,
            button_label=_("Continue"),
        )

    def final_score_message(self, session: Session):
        """Create final score message for given session"""

        n_sync_guessed = 0
        sync_time = 0
        n_sync_correct = 0
        n_old_new_expected = 0
        n_old_new_correct = 0

        for result in session.result_set.all():
            if result.question_key == "recognize":
                if result.given_response == "yes":
                    n_sync_guessed += 1
                    json_data = result.json_data
                    sync_time += json_data.get("decision_time")
                    if result.score > 0:
                        n_sync_correct += 1
            else:
                if result.expected_response == "old":
                    n_old_new_expected += 1
                    if result.score > 0:
                        n_old_new_correct += 1

        score_message = "Well done!" if session.final_score > 0 else "Too bad!"
        if n_sync_guessed == 0:
            song_sync_message = "You did not recognise any songs at first."
        else:
            song_sync_message = "It took you {} s to recognise a song on average, and you correctly identified {} out of the {} songs you thought you knew.".format(
                round(sync_time / n_sync_guessed, 1), n_sync_correct, n_sync_guessed
            )
        heard_before_message = "During the bonus rounds, you remembered {} of the {} songs that came back.".format(
            n_old_new_correct, n_old_new_expected
        )
        return score_message + " " + song_sync_message + " " + heard_before_message

    def get_trial_title(self, session: Session, round_number):
        return _("Round %(number)d / %(total)d") % {"number": round_number, "total": session.block.rounds}

    def plan_sections(self, session: Session):
        """Set the plan of tracks for a session."""
        # Get available songs and pick a section for each
        n_rounds = session.block.rounds

        # How many sections do we need?
        # 2/3 of the rounds are SongSync, of which 1/4 songs will return, 3/4 songs are "free", i.e., won't return
        # 1/3 of the rounds are "heard before", of which 1/2 old songs
        # e.g. 30 rounds -> 20 SongSync with 5 songs to be repeated later
        n_song_sync_rounds = round(2 / 3 * n_rounds)
        n_returning_rounds = round(1 / 4 * n_song_sync_rounds)
        song_sync_condtions = ["returning"] * n_returning_rounds + ["free"] * (n_song_sync_rounds - n_returning_rounds)
        random.shuffle(song_sync_condtions)
        n_heard_before_rounds = n_rounds - n_song_sync_rounds
        n_heard_before_rounds_old = round(0.5 * n_heard_before_rounds)
        n_heard_before_rounds_new = n_heard_before_rounds - n_heard_before_rounds_old
        heard_before_conditions = ["old"] * n_heard_before_rounds_old + ["new"] * n_heard_before_rounds_new
        random.shuffle(heard_before_conditions)
        plan = song_sync_condtions + heard_before_conditions

        # Save, overwriting existing plan if one exists.
        session.save_json_data({"plan": plan, "heard_before_offset": n_song_sync_rounds})

    def select_song_sync_section(self, session: Session, condition, filter_by={}) -> Section:
        """Return a section for the song_sync round
        parameters:
            - session
            - condition: can be "new" or "returning"
            - filter_by: may be used to filter sections
        """
        return session.playlist.get_section(filter_by, song_ids=session.get_unused_song_ids())

    def next_song_sync_action(self, session: Session, round_number: int) -> Trial:
        """Get next song_sync section for this session."""
        try:
            plan = session.json_data["plan"]
        except KeyError as error:
            logger.error("Missing plan key: %s" % str(error))
            return None

        condition = plan[round_number]
        section = self.select_song_sync_section(session, condition)
        if condition == "returning":
            played_sections = session.json_data.get("played_sections", [])
            played_sections.append(section.id)
            session.save_json_data({"played_sections": played_sections})
        return song_sync(
            session,
            section,
            title=self.get_trial_title(session, round_number + 1),
            recognition_time=self.recognition_time,
            sync_time=self.sync_time,
            min_jitter=self.min_jitter,
            max_jitter=self.max_jitter,
        )

    def select_heard_before_section(self, session: Session, condition: str, filter_by={}) -> Section:
        """select a section for the `heard_before` rounds
        parameters:
            - session
            - condition: 'old' or 'new'
            - filter_by: dictionary to restrict the types of sections returned, e.g., to play a section with a different tag
        """
        if condition == "old":
            current_section_id = self.get_returning_section_id(session)
            return Section.objects.get(pk=current_section_id)
        else:
            song_ids = session.get_unused_song_ids()
            return session.playlist.get_section(filter_by, song_ids=song_ids)

    def get_returning_section_id(self, session: Session) -> int:
        """read the list of `played_sections`, select and return a random item,
        save `played_sections` without this item
        """
        played_sections = session.json_data.get("played_sections")
        random.shuffle(played_sections)
        current_section_id = played_sections.pop()
        session.save_json_data({"played_sections": played_sections})
        return current_section_id

    def next_heard_before_action(self, session: Session, round_number: int) -> Trial:
        """Get next heard_before action for this session."""
        # Load plan.
        try:
            plan = session.json_data["plan"]
        except KeyError as error:
            logger.error("Missing plan key: %s" % str(error))
            return None
        # Get section.
        condition = plan[round_number]
        section = self.select_heard_before_section(session, condition)
        playback = Autoplay([section], show_animation=True, preload_message=_("Get ready!"))
        # create Result object and save expected result to database
        key = "heard_before"
        form = Form(
            [
                BooleanQuestion(
                    key=key,
                    choices={
                        "new": _("No"),
                        "old": _("Yes"),
                    },
                    question=_("Did you hear this song in previous rounds?"),
                    result_id=prepare_result(
                        key,
                        session,
                        section=section,
                        expected_response=condition,
                        scoring_rule="REACTION_TIME",
                    ),
                    submits=True,
                    style=[ColorScheme.BOOLEAN_NEGATIVE_FIRST, ButtonStyle.LARGE_GAP],
                )
            ]
        )
        config = {"auto_advance": True, "response_time": self.heard_before_time}
        trial = Trial(
            title=self.get_trial_title(session, round_number + 1),
            playback=playback,
            feedback_form=form,
            config=config,
        )
        return trial

    def get_score(self, session: Session, round_number: int) -> Score:
        config = {"show_section": True, "show_total_score": True}
        title = self.get_trial_title(session, round_number)
        previous_result = session.last_result(self.counted_result_keys)
        return Score(session, config=config, title=title, result=previous_result)
