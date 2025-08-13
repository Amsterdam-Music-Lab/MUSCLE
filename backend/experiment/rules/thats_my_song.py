from os.path import basename, splitext

from django.utils.translation import gettext_lazy as _

from experiment.actions import Final, Trial
from experiment.actions.form import Form, ChoiceQuestion
from question.questions import QUESTION_GROUPS
from result.utils import prepare_result
from section.models import Section
from session.models import Session
from .hooked import Hooked


class ThatsMySong(Hooked):
    ID = "THATS_MY_SONG"
    consent_file = ""

    def __init__(self):
        self.question_series = [
            {"name": "DEMOGRAPHICS", "keys": ["dgf_generation", "dgf_gender_identity"], "randomize": False},
            {"name": "MUSICGENS_17_W_VARIANTS", "keys": QUESTION_GROUPS["MUSICGENS_17_W_VARIANTS"], "randomize": True},
        ]

    def feedback_info(self):
        return None

    def get_info_playlist(self, section_path):
        """function used by `manage.py compileplaylist` to compile a csv with metadata"""
        filename = splitext(basename(section_path))[0]
        parts = filename.split(" - ")
        time_info = int(parts[0])
        if time_info < 1970:
            decade = "1960s"
        elif time_info < 1980:
            decade = "1970s"
        elif time_info < 1990:
            decade = "1980s"
        elif time_info < 2000:
            decade = "1990s"
        else:
            decade = "2000s"
        try:
            int(parts[-1])
            form = parts[-2]
        except:
            form = parts[-1]
        return {"artist": parts[1], "song": parts[2], "tag": form, "group": decade}

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
            return [
                self.get_score(session, round_number),
                Final(
                    session=session,
                    final_text=self.final_score_message(session)
                    + " For more information about this experiment, visit the Vanderbilt University Medical Center Music Cognition Lab.",
                    rank=self.rank(session),
                    show_profile_link=True,
                    button={
                        "text": _("Play again"),
                        "link": self.get_play_again_url(session),
                    },
                    logo={
                        "image": "/images/vumc_mcl_logo.png",
                        "link": "https://www.vumc.org/music-cognition-lab/welcome",
                    },
                ),
            ]

        if round_number == 0:
            # get list of trials for demographic questions (first 2 questions)
            if session.result_set.filter(question_key="playlist_decades").count() == 0:
                actions = [self.get_intro_explainer()]
                questions = self.get_open_questions(session, cutoff_index=2)
                if questions:
                    for q in questions:
                        actions.append(q)

                question = ChoiceQuestion(
                    key="playlist_decades",
                    view="CHECKBOXES",
                    question=_("Choose two or more decades of music"),
                    choices={"1960s": "1960s", "1970s": "1970s", "1980s": "1980s", "1990s": "1990s", "2000s": "2000s"},
                    min_values=2,
                    result_id=prepare_result("playlist_decades", session=session),
                )
                actions.append(Trial(title=_("Playlist selection"), feedback_form=Form([question])))
                return actions

            # Go to SongSync
            else:
                self.plan_sections(session)
                return self.next_song_sync_action(session, round_number)
        else:
            # Create a score action.
            actions = [self.get_score(session, round_number)]
            heard_before_offset = session.json_data.get("heard_before_offset")
            # no rounds without questions if the player has previously played
            question_offset = (
                0 if self.has_played_before(session) else self.question_offset
            )

            # SongSync rounds. Skip questions until round defined in question_offset.
            if round_number in range(1, question_offset):
                actions.extend(self.next_song_sync_action(session, round_number))
            if round_number in range(question_offset, heard_before_offset):
                question = self.get_single_question(session, randomize=True)
                if question:
                    actions.append(question)
                actions.extend(self.next_song_sync_action(session, round_number))

            # HeardBefore rounds
            if round_number == heard_before_offset:
                # Introduce new round type with Explainer.
                actions.append(self.heard_before_explainer())
                actions.append(self.next_heard_before_action(session, round_number))
            if round_number > heard_before_offset:
                question = self.get_single_question(session, randomize=True)
                if question:
                    actions.append(question)
                actions.append(self.next_heard_before_action(session, round_number))

        return actions

    def select_song_sync_section(self, session: Session, condition: str) -> Section:
        decades = session.result_set.first().given_response.split(",")
        return super().select_song_sync_section(session, condition, filter_by={"group__in": decades})

    def select_heard_before_section(self, session: Session, condition: str) -> Section:
        decades = session.result_set.first().given_response.split(",")
        return super().select_heard_before_section(session, condition, filter_by={"group__in": decades})
