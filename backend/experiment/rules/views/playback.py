class Playback(object):
    ''' A playback wrapper for different kinds of players
        - player_type: can be one of the following:
            - 'AUTOPLAY' - player starts automatically
            - 'BUTTON' - display one play button
            - 'MULTIPLAYER' - display multiple small play buttons, one per section
        - sections: a list of sections (in many cases, will only contain *one* section)
        - preload_message: text to display during preload
        - instruction: text to display during presentation of the sound
        - config: define to override the following values:
            - ready_time: time before presentation of sound
            - decision_time: maximum time that participant can take (only relevant when auto_advance=True)
            - playhead: from where the audio file should play (offset in seconds from start)
            - mute: whether audio should be muted
            - auto_advance: whether the view will switch to next view after decision_time
            - auto_play: whether sound will start automatically
            - show_animation: whether to show an animation during playback '''
    def __init__(self, player_type, sections, preload_message='', instruction='', play_config=None):
        self.player_type = player_type
        self.sections = [{'id': s.id, 'url': s.absolute_url()} for s in sections]
        self.preload_message = preload_message
        self.instruction = instruction
        self.play_config = {
            'ready_time': 0,
            'decision_time': 5,
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
            'play_config': self.play_config
        }
        return action
