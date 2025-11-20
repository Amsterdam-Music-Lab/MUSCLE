from django.utils.translation import gettext_lazy as _
from typing import Optional, TypedDict

from .base_action import BaseAction
from .button import Button
from experiment.actions.form import Form
from experiment.actions.html import HTML
from experiment.actions.playback import Playback


class BreakRoundOn(TypedDict):
    EQUALS: list[str]
    NOT: list[str]


class Trial(BaseAction):  # pylint: disable=too-few-public-methods
    """
    A view that may include Playback and/or a Form to be displayed to the participant.

    Args:
        playback (Optional[Playback]): Player(s) to be displayed in this view (e.g. audio, video, image)
        html (Optional[str]): HTML to be displayed in this view
        feedback_form (Optional[Form]): array of form elements
        title (Optional(str)): page title - defaults to empty
        response_time (int): time in seconds for the participant to react
        auto_advance (bool): whether the view automatically forwards to the next after response_time
        listen_first (bool): whether the controls are blocked while audio is playing
        continue_button (Button): optionally configure label and color of button below the Trial. Not shown if form with submit_button is passed. Set to `None` to suppress such a button.
        break_round_on (dict): conditions under which the current round should be abandoned, to query `session/next_round` for new actions


    Example:
        ```python
        key = 'test_trial'
        section = session.playlist.get_section()
        question = BooleanQuestion(
            text=_(
                "Do you like this song?"),
            key=key,
            result_id=prepare_result(key, session, section=section),
        )
        form = Form([question])
        playback = Autoplay([section])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Test block'),
        )
        ```

    Note:
        Relates to client component: Trial.tsx
    """

    view = "TRIAL_VIEW"

    def __init__(
        self,
        playback: Optional[Playback] = None,
        html: Optional[HTML] = None,
        feedback_form: Optional[Form] = None,
        title: str = "",
        response_time: float = 5.0,
        auto_advance: bool = False,
        listen_first: bool = False,
        continue_button: Optional[Button] = Button(_("Continue"), "colorPrimary"),
        break_round_on: Optional[BreakRoundOn] = None,
    ):
        self.playback = playback
        self.html = html
        self.feedback_form = feedback_form
        self.title = title
        self.response_time = response_time
        self.auto_advance = auto_advance
        self.listen_first = listen_first
        self.continue_button = continue_button
        self.break_round_on = break_round_on

    def action(self):
        """
        Serialize data for a block action

        """
        # Create action
        action = {
            "view": self.view,
            "title": self.title,
            "responseTime": self.response_time,
            "autoAdvance": self.auto_advance,
            "listenFirst": self.listen_first,
            "breakRoundOn": self.break_round_on,
        }
        if self.button:
            action["continueButton"] = self.continue_button.action()
        if self.playback:
            action["playback"] = self.playback.action()
        if self.html:
            action["html"] = self.html.action()
        if self.feedback_form:
            action["feedbackForm"] = self.feedback_form.action()

        return action
