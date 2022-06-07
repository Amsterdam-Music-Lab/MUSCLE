from django.utils.translation import gettext_lazy as _

from .form import ChoiceQuestion, Form

class Trial(object):  # pylint: disable=too-few-public-methods
    """
    A view that may include Playback and/or a Form
    Relates to client component: Trial.js

    Parameters:
    - section: section to be played in this view
    - feedback_form: array of form elements
    - instructions: messages to show during different stages - defaults to Hooked instructions
    - title: page title - defaults to empty
    """

    ID = 'TRIAL_VIEW'

    def __init__(self, playback=None, feedback_form=None, title='', config=None):
        '''
        - playback: Playback object (may be None)
        - feedback_form: Form object (may be None)
        - title: string setting title in header of experiment
        - config: dictionary with following settings
            - decision_time: how long to wait until stopping the player / proceeding to the next view
            - auto_advance: proceed to next view after player has stopped
            - listen_first: whether participant can submit before end of sound
            - style: style class to add to elements in form and playback
                - neutral: first element is blue, second is yellow, third is teal
                - neutral-inverted: first element is yellow, second is blue, third is teal
                - boolean: first element is green, second is red
            - time_pass_break: when time has passed, submit the result immediately; skipping any subsequent actions (e.g. a certainty question)
                - Can not be combined with listen_first (True)
                - Can not be combined with auto_advance (False)
            - continue_label: if there is no form, how to label a button to proceed to next view
        '''
        self.playback = playback
        self.feedback_form = feedback_form
        self.title = title
        self.config = {
            'decision_time': 5,
            'auto_advance': False,
            'listen_first': False,
            'continue_label': _('Continue'),
            'style': 'neutral'
        }
        if config:
            self.config.update(config)


    def action(self):
        """
        Serialize data for experiment action

        """
        # Create action
        action = {
            'view': Trial.ID,
            'title': self.title,
            'config': self.config,
        }
        if self.playback:
            action['playback'] = self.playback.action()
        if self.feedback_form:
            action['feedback_form'] = self.feedback_form.action()

        return action
