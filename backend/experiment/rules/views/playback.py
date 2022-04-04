class Playback(object):
    ''' A playback wrapper for different kinds of players
        - player_type: can be one of the following:
            - 'AUTOPLAY' - player starts automatically
            - 'BUTTON' - display one play button
            - 'MULTIPLAYER' - display multiple small play buttons, one per section
        - sections: a list of sections (in many cases, will only contain *one* section)
        - instructions: any text to display during preload or presentation
        - config: define to override the following values:
            - ready_time: time before presentation of sound
            - decision_time: maximum time that participant can take (only relevant when auto_advance=True)
            - playhead: from where the audio file should play (offset in seconds from start)
            - mute: whether audio should be muted
            - auto_advance: whether the view will switch to next view after decision_time
            - auto_play: whether sound will start automatically
            - show_animation: whether to show an animation during playback '''
    def __init__(self, sections, player_type='AUTOPLAY', preload_message='', instruction='', play_config=None):
        self.sections = [{'id': s.id, 'url': s.absolute_url()} for s in sections]
        self.player_type = player_type
        self.preload_message = preload_message
        self.instruction = instruction
        self.play_config = {
            'ready_time': 0,
            'playhead': 0,
            'show_animation': False,
            'mute': False
        }
        if play_config:
            self.play_config.update(play_config)

    def action(self):
        action = {
            'player_type': self.player_type,
            'sections': self.sections,
            'instruction': self.instruction,
            'preload_message': self.preload_message,
            'play_config': self.play_config
        }
        return action
