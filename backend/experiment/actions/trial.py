from django.utils.translation import gettext_lazy as _
from typing import Optional, TypedDict

from .base_action import BaseAction
from experiment.actions.form import Form
from experiment.actions.playback import Playback


class Config(TypedDict):
    """
    Configuration for the Trial action.

    Args:
      - response_time (int): how long to wait until stopping the player
      - auto_advance (bool): proceed automatically after stopping
      - listen_first (bool): block form submission until playback ends
      - show_continue_button (bool): display a 'Continue' button
      - continue_label (str): label for the continue button
    """

    response_time: int
    auto_advance: bool
    listen_first: bool
    show_continue_button: bool
    continue_label: str


class Trial(BaseAction):  # pylint: disable=too-few-public-methods
    """
    A view that may include Playback and/or a Form to be displayed to the participant.

    Args:
        playback (Optional[Playback]): Player(s) to be displayed in this view (e.g. audio, video, image)
        html (Optional[str]): HTML to be displayed in this view
        feedback_form (Optional[Form]): array of form elements
        title (Optional(str)): page title - defaults to empty
        config (Optional[Config]): configuration for the trial with options for response time, auto advance, listen first, show continue button, and continue label

    Example:
        ```python
        key = 'test_trial'
        section = session.playlist.get_section()
        question = BooleanQuestion(
            question=_(
                "Do you like this song?"),
            key=key,
            result_id=prepare_result(key, session, section=section),
            submits=True
        )
        form = Form([question])
        playback = Autoplay([section])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Test block'),
            config={
                'response_time': section.duration,
                'listen_first': True
            }
        )
        ```

    Note:
        Relates to client component: Trial.tsx
    """

    view = "TRIAL_VIEW"

    def __init__(
        self,
        playback: Optional[Playback] = None,
        html: Optional[str] = None,
        feedback_form: Optional[Form] = None,
        title="",
        config: Optional[Config] = None,
    ):
        self.playback = playback
        self.html = html
        self.feedback_form = feedback_form
        self.title = title
        self.config = {
            "response_time": 5,
            "auto_advance": False,
            "listen_first": False,
            "show_continue_button": True,
            "continue_label": _("Continue"),
        }
        if config:
            self.config.update(config)

    def action(self):
        """
        Serialize data for a block action

        """
        # Create action
        action = {
            "view": self.view,
            "title": self.title,
            "config": self.config,
        }
        if self.playback:
            action["playback"] = self.playback.action()
        if self.html:
            action["html"] = self.html.action()
        if self.feedback_form:
            action["feedback_form"] = self.feedback_form.action()

        return action
