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

    def __init__(self, section, feedback_form, instructions=None, title=''):
        self.section = section
        self.feedback_form = feedback_form
        self.instructions = INSTRUCTIONS_DEFAULT
        if instructions:
            self.instructions.update(instructions)
        self.title = title
        self.listen_first = listen_first

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
            'feedback_form': self.feedback_form,
            'title': self.title,
            'instructions': self.instructions
        }

        # Section
        if self.section:
            action['section'] = {
                'id': self.section.id,
                'url': self.section.absolute_url(),
            }
        
        # advance automatically if there is no form, i.e., no user interaction
        auto_advance = False if self.feedback_form else True

        # Config
        action['config'] = {
            'ready_time': 0,
            'decision_time': 5,
            'auto_advance': auto_advance,
            'auto_play': True,
            'listen_first': False,
        }
        self.config.update(config)
        
        # advance automatically if there is no form, i.e., no user interaction
        if not self.feedback_form:
            self.config.auto_advance = True 

        return action