from django.utils.translation import gettext_lazy as _

INSTRUCTIONS_DEFAULT = {
    'during_presentation': _('Do you recognise this song?'),
    'during_silence': _('Keep imagining the music'),
    'after_trial': _('Did the track come back in the right place?'),
    'preload': _('Get ready!')
}

class CompositeView:  # pylint: disable=too-few-public-methods
    """
    Provide data for a view that plays a section, and shows a form

    Relates to client component: CompositeView.js

    Parameters:
    - section: section to be played in this view
    - feedback_form: array of form elements
    - instructions: messages to show during different stages - defaults to Hooked instructions
    - title: page title - defaults to empty
    """

    ID = 'COMPOSITE_VIEW'

    def __init__(self, playback, feedback_form, title=''):
        self.playback = playback
        self.feedback_form = feedback_form
        self.title = title

    def action(self, config={}):
        """
        Get data for experiment action
        action['section']: information on the section
        pass in a config dictionary to override the following values:
        - ready_time: time before presentation of sound
        - decision_time: maximum time that participant can take (only relevant when auto_advance=True)
        - auto_advance: whether the view will switch to next view after decision_time
        - auto_play: whether sound will start automatically
        - listen_first: whether participant can submit before end of sound
        - time_pass_break: when time has passed, submit the result immediately; skipping any subsequent actions (e.g. a certainty question)
            - Can not be combined with listen_first (True)
            - Can not be combined with auto_advance (False)
        - show_animdation: whether to show an animation during playback
        """
        # Create action
        action = {
            'view': CompositeView.ID,
            'title': self.title,
        }
        if self.playback:
            action['playback'] = self.playback.action()
        if self.feedback_form:
            action['feedback_form'] = self.feedback_form.action()
        
        return action