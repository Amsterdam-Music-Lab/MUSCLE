from django.utils.translation import gettext_lazy as _


INSTRUCTIONS_DEFAULT = {
    'during_presentation': _('Do you recognise this song?'),
    'during_silence': _('Keep imagining the music'),
    'after_trial': _('Did the track come back in the right place?'),
    'preload': _('Get ready!')
}

class Playback(object):
    ''' A playback wrapper for different kinds of players
        pass in a config dictionary to override the following values:
        - ready_time: time before presentation of sound
        - decision_time: maximum time that participant can take (only relevant when auto_advance=True)
        - auto_advance: whether the view will switch to next view after decision_time
        - auto_play: whether sound will start automatically

        - show_animdation: whether to show an animation during playback '''
    def __init__(self, player_type, sections, instructions=None, config=None):
        self.player_type = player_type
        self.sections = [{'id': s.id, 'url': s.absolute_url()} for s in sections]
        self.instructions = INSTRUCTIONS_DEFAULT
        if instructions:
            self.instructions.update(instructions)
        self.config = {
            'ready_time': 0,
            'decision_time': 5,
            'show_animation': False
        }
        if config:
            self.config.update(config)
    
    def action(self):
        # # advance automatically if there is no form, i.e., no user interaction
        # auto_advance = False if self.feedback_form else True

        
        # # advance automatically if there is no form, i.e., no user interaction
        # if not self.feedback_form:
        #     self.config.auto_advance = True


        action = {
            'player_type': self.player_type,
            'sections': self.sections,
            'instructions': self.instructions,
            'config': self.config
        }
        
        return action