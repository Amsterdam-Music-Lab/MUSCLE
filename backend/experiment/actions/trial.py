from django.utils.translation import gettext_lazy as _
from typing import Optional, TypedDict

from .base_action import BaseAction
from experiment.actions.form import Form
from experiment.actions.playback import Playback
from .frontend_style import FrontendStyle


class Config(TypedDict):
    """
    Configuration for the Trial action

    Args:
        response_time: how long to wait until stopping the player / proceeding to the next view
        auto_advance: proceed to next view after player has stopped
        listen_first: whether participant can submit before end of sound
        show_continue_button: whether to show a button to proceed to the next view
        continue_label: label for the continue button
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
        config (Optional[Config]): dictionary with following settings
        style (FrontendStyle): style class to add to elements in form and playback
            neutral: first element is blue, second is yellow, third is teal
            neutral-inverted: first element is yellow, second is blue, third is teal
            boolean: first element is green, second is red
            boolean-negative-first: first element is red, second is green

    Note:
        Relates to client component: Trial.tsx
    """

    ID = "TRIAL_VIEW"

    def __init__(
        self,
        playback: Optional[Playback] = None,
        html: Optional[str] = None,
        feedback_form: Optional[Form] = None,
        title="",
        config: Optional[Config] = None,
        style: FrontendStyle = FrontendStyle(),
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
        self.style = style

    def action(self):
        """
        Serialize data for a block action

        """
        # Create action
        action = {
            "view": Trial.ID,
            "title": self.title,
            "config": self.config,
        }
        if self.style:
            action["style"] = self.style.to_dict()
        if self.playback:
            action["playback"] = self.playback.action()
        if self.html:
            action["html"] = self.html.action()
        if self.feedback_form:
            action["feedback_form"] = self.feedback_form.action()

        return action
