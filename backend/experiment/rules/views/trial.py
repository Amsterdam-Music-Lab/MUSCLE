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
            - time_pass_break: when time has passed, submit the result immediately; skipping any subsequent actions (e.g. a certainty question)
                - Can not be combined with listen_first (True)
                - Can not be combined with auto_advance (False)
        '''
        self.playback = playback
        self.feedback_form = feedback_form
        self.title = title
        self.config = {
            'decision_time': 5,
            'auto_advance': False,
            'listen_first': False,
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


class TwoAlternativeForced(Trial):
    """
    Provide data for a TwoAlternativeForced view that (auto)plays a section,
    shows a question and has two customizable buttons
    """
    def __init__(self, sections, show_button_labels=False, **kwargs):
        super().__init__(**kwargs)
        self.playback = Playback(
            sections,
            'MULTIPLAYER'
        )
        question = ChoiceQuestion(
            choices = {'section.id': section.name for section in sections},
            view='BUTTON_ARRAY'
        )
        self.feedback_form = Form([question])
        self.config['show_button_labels'] = show_button_labels
