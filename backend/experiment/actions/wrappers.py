import random
from typing import Optional

from django.utils.translation import gettext as _

from .button import Button
from .final import Final
from .form import Form
from .playback import Autoplay, PlayButtons, PlaybackSection
from .trial import Trial
from .utils import get_current_experiment_url

from experiment.actions.utils import randomize_playhead
from experiment.actions.question import ButtonArrayQuestion
from question.models import ChoiceList
from result.utils import prepare_result
from section.models import Section
from session.models import Session
from theme.styles import ButtonStyle, ColorScheme, TextStyle

class TwoAlternativeForced(Trial):
    """
    Args:
        session (Session): Session for which to generate TwoAlternativeForced Trial
        section (Section): Section to be played in TwoAlternativeForced Trial
        choices (dict): choices to be presented to participant
        expected_response (str): expected response, if applicable
        comment (str): comment to be logged with the result
        scoring_rule: scoring rule to score the participant's response
        **kwargs: additional arguments to initialize the Trial object (e.g., response_time)

    Returns:
        (Trial): Configured trial containing a playback, a question, and a feedback form.

    Example:
        ```python
        trial = two_alternative_forced(session, section, {"yes": "Yes", "no": "No"}, expected_response="yes", title=_("Two Alternative Forced Choice"))
        ```
    """

    def __init__(
        self,
        session: Session,
        section: Section,
        choices: dict,
        expected_response: Optional[str] = None,
        comment: str = "",
        scoring_rule: Optional[str] = None,
        style: list[str] = [],
        **kwargs
    ):
        playback = PlayButtons(sections=[PlaybackSection(section)], play_once=True)
        key = "choice"
        button_style = [
            TextStyle.INVISIBLE,
            ButtonStyle.LARGE_GAP,
            ButtonStyle.LARGE_TEXT,
        ]
        button_style.extend(style)
        question = ButtonArrayQuestion(
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
            style=button_style,
        )
        feedback_form = Form([question], submit_button=None)
        super().__init__(playback=playback, feedback_form=feedback_form, **kwargs)


def boolean_question(
    key: str,
    text: str,
    result_id: int,
    style=[ColorScheme.BOOLEAN_NEGATIVE_FIRST, ButtonStyle.LARGE_GAP],
):
    return ButtonArrayQuestion(
        key=key,
        text=text,
        result_id=result_id,
        choices=ChoiceList.objects.get(pk='BOOLEAN_NEGATIVE_FIRST').to_dict(),
        style=style,
    )


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
    recognize = Trial(
        feedback_form=Form(
            [
                boolean_question(
                    key='recognize',
                    text='',
                    result_id=prepare_result(
                        "recognize",
                        session,
                        section=section,
                        scoring_rule="SONG_SYNC_RECOGNITION",
                    ),
                )
            ],
            submit_button=Button(""),
        ),
        playback=Autoplay(
            sections=[PlaybackSection(section)],
            show_animation=True,
            preload_message=_("Get ready!"),
            instruction=_("Do you recognize the song?"),
        ),
        response_time=recognition_time,
        auto_advance=True,
        break_round_on={"EQUALS": ["TIMEOUT", "no"]},
        title=title,
    )
    silence_time = 4
    silence = Trial(
        playback=Autoplay(
            sections=[PlaybackSection(section, mute=True)],
            show_animation=True,
            instruction=_("Keep imagining the music"),
        ),
        response_time=silence_time,
        auto_advance=True,
        continue_button=None,
        title=title,
    )
    continuation_correctness = random.choice([True, False])
    jitter = randomize_playhead(min_jitter, max_jitter, continuation_correctness)
    correct_place = Trial(
        feedback_form=Form(
            [
                boolean_question(
                    key="correct_place",
                    text="",
                    result_id=prepare_result(
                        "correct_place",
                        session,
                        section=section,
                        scoring_rule="SONG_SYNC_VERIFICATION",
                        json_data={"continuation_offset": jitter},
                        expected_response="yes" if continuation_correctness else "no",
                    ),
                )
            ]
        ),
        playback=Autoplay(
            sections=[PlaybackSection(section, play_from=silence_time + jitter)],
            instruction=_("Did the track come back in the right place?"),
            show_animation=True,
            resume_play=True,
        ),
        response_time=sync_time,
        title=title,
    )
    return [recognize, silence, correct_place]

def final_action_with_optional_button(session, final_text="", title=_("End"), button_text=_("Continue")) -> Final:
    """
    Description: Create a final action with an optional button to proceed to the next block, if available.

    Args:
        session (Session): The current session.
        final_text (str): The text to display in the final action.
        title (str): The title for the final action screen.
        button_text (str): The text displayed on the continuation button.

    Returns:
        (Final): The final action with an optional button.

    Example:
        ```python
        action = final_action_with_optional_button(my_session, final_text="Complete!")
        ```
    """
    redirect_url = get_current_experiment_url(session)

    if redirect_url:
        return Final(
            title=title,
            session=session,
            final_text=final_text,
            button=Button(button_text, link=redirect_url),
        )
    else:
        return Final(
            title=title,
            session=session,
            final_text=final_text,
        )
