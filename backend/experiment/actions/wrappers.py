import random
from typing import Optional

from django.utils.translation import gettext as _

from .form import BooleanQuestion, ChoiceQuestion, Form
from .styles import ButtonStyle, TextStyle
from .playback import Autoplay, PlayButton
from .trial import Trial

from experiment.actions.utils import randomize_playhead
from result.utils import prepare_result
from section.models import Section
from session.models import Session


def two_alternative_forced(
    session: Session,
    section: Section,
    choices: dict,
    expected_response: str = None,
    style: list[str] = None,
    comment: str = "",
    scoring_rule: str = None,
    title: str = "",
    config: Optional[dict] = None,
):
    """
    Description: Provide data for a two-alternative forced choice (2AFC) view, with an optional comment and scoring.

    Args:
        session (Session): Current user session.
        section (Section): Section to use in the playback or question.
        choices (dict): Possible choices presented to the user.
        expected_response (str, optional): The expected user response.
        style (dict, optional): Additional style configurations for buttons.
        comment (str, optional): Comment or additional info about the session.
        scoring_rule (str, optional): Rule for scoring the user's response.
        title (str, optional): Title to be displayed in the trial.
        config (dict, optional): Additional configuration parameters.

    Returns:
        (Trial): Configured trial containing a playback, a question, and a feedback form.

    Example:
        ```python
        trial = two_alternative_forced(session, section, {"yes": "Yes", "no": "No"}, expected_response="yes", title=_("Two Alternative Forced Choice"))
        ```
    """
    playback = PlayButton([section], {"listen_once": True})
    key = "choice"
    button_style = [TextStyle.INVISIBLE, ButtonStyle.LARGE_GAP, ButtonStyle.LARGE_TEXT]
    button_style.extend(style)
    question = ChoiceQuestion(
        key=key,
        result_id=prepare_result(
            key,
            session=session,
            section=section,
            expected_response=expected_response,
            scoring_rule=scoring_rule,
            comment=comment,
        ),
        choices=choices,
        view="BUTTON_ARRAY",
        submits=True,
        style=button_style,
    )
    feedback_form = Form([question])
    trial = Trial(playback=playback, feedback_form=feedback_form, title=title, config=config)
    return trial


def song_sync(
    session: Session, section: Section, title: str, recognition_time=15, sync_time=15, min_jitter=10, max_jitter=15
):
    """
    Description: Provide a series of Trials for song recognition and sync, including optional jitter.

    Args:
        session (Session): Current user session.
        section (Section): Section to use for playback and silence intervals.
        title (str): Title to be displayed for the trials.
        recognition_time (int, optional): Response time for recognition.
        sync_time (int, optional): Response time for syncing continuation.
        min_jitter (int, optional): Minimum playback offset for continuation correctness trial.
        max_jitter (int, optional): Maximum playback offset for continuity trial.

    Returns:
        (list): A list of Trials (recognize, silence, correct_place).

    Example:
        ```python
        trials = song_sync(session, section, _("Song Sync"), recognition_time=10)
        ```
    """
    trial_config = {"response_time": recognition_time, "auto_advance": True}
    recognize = Trial(
        feedback_form=Form(
            [
                BooleanQuestion(
                    key="recognize",
                    result_id=prepare_result(
                        "recognize", session, section=section, scoring_rule="SONG_SYNC_RECOGNITION"
                    ),
                    submits=True,
                )
            ]
        ),
        playback=Autoplay(
            [section],
            show_animation=True,
            preload_message=_("Get ready!"),
            instruction=_("Do you recognize the song?"),
        ),
        config={**trial_config, "break_round_on": {"EQUALS": ["TIMEOUT", "no"]}},
        title=title,
    )
    silence_time = 4
    silence = Trial(
        playback=Autoplay([section], show_animation=True, instruction=_("Keep imagining the music"), mute=True),
        config={
            "response_time": silence_time,
            "auto_advance": True,
            "show_continue_button": False,
        },
        title=title,
    )
    continuation_correctness = random.choice([True, False])
    jitter = randomize_playhead(min_jitter, max_jitter, continuation_correctness)
    trial_config["response_time"] = sync_time
    correct_place = Trial(
        feedback_form=Form(
            [
                BooleanQuestion(
                    key="correct_place",
                    submits=True,
                    result_id=prepare_result(
                        "correct_place",
                        session,
                        section=section,
                        scoring_rule="SONG_SYNC_CONTINUATION",
                        json_data={"continuation_offset": jitter},
                        expected_response="yes" if continuation_correctness else "no",
                    ),
                )
            ]
        ),
        playback=Autoplay(
            [section],
            instruction=_("Did the track come back in the right place?"),
            show_animation=True,
            play_from=silence_time + jitter,
            resume_play=True,
        ),
        config=trial_config,
        title=title,
    )
    return [recognize, silence, correct_place]
