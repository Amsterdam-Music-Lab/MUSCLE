from django.utils.translation import gettext_lazy as _


INSTRUCTIONS_DEFAULT = {
    'during_presentation': _('Do you recognise this song?'),
    'during_silence': _('Keep imagining the music'),
    'after_trial': _('Did the track come back in the right place?'),
    'preload': _('Get ready!')
}

class Playback(object):
    ''' A playback wrapper for different kinds of players '''
    def __init__(self, player_type, sections, instructions=None, config=None):
        self.player_type = player_type
        self.sections = sections
        self.instructions = INSTRUCTIONS_DEFAULT
        if instructions:
            self.instructions.update(instructions)
        self.config = {
            'ready_time': 0,
            'decision_time': 5,
            'auto_advance': False,
            'auto_play': True,
            'listen_first': False,
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