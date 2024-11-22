from django.utils.translation import gettext_lazy as _

from .base_action import BaseAction
from experiment.actions.form import Form
from experiment.actions.playback import Playback
from .frontend_style import FrontendStyle


class Trial(BaseAction):  # pylint: disable=too-few-public-methods
    """
    A view that may include Playback and/or a Form
    Relates to client component: Trial.js

    Parameters:
    - playback: player(s) to be displayed in this view
    - feedback_form: array of form elements
    - title: page title - defaults to empty
    """

    ID = "TRIAL_VIEW"

    def __init__(
        self,
        playback: Playback = None,
        html: str = None,
        feedback_form: Form = None,
        title="",
        config: dict = None,
        style: FrontendStyle = FrontendStyle(),
    ):
        """
        - playback: Playback object (may be None)
        - html: HTML object (may be None)
        - feedback_form: Form object (may be None)
        - title: string setting title in header of experiment
        - config: dictionary with following settings
            - response_time: how long to wait until stopping the player / proceeding to the next view
            - auto_advance: proceed to next view after player has stopped
            - listen_first: whether participant can submit before end of sound
            - break_round_on: result values upon which consecutive rounds in the current next_round array will be skipped
            - continue_label: if there is no form, how to label a button to proceed to next view
        - style: style class to add to elements in form and playback
            - neutral: first element is blue, second is yellow, third is teal
            - neutral-inverted: first element is yellow, second is blue, third is teal
            - boolean: first element is green, second is red
            - boolean-negative-first: first element is red, second is green
        """
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
