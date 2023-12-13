from .base_action import BaseAction

class Playback(BaseAction):
    ''' A playback wrapper for different kinds of players
        - player_type: can be one of the following:
            - 'AUTOPLAY' - player starts automatically
            - 'BUTTON' - display one play button
            - 'MULTIPLAYER' - display multiple small play buttons, one per section
            - 'SPECTROGRAM' - extends multiplayer with a list of spectrograms
        - sections: a list of sections (in many cases, will only contain *one* section)
        - preload_message: text to display during preload
        - instruction: text to display during presentation of the sound
        - play_config: define to override the following values:
            - play_method:
                - 'BUFFER': Use webaudio buffers. (recommended for stimuli up to 45s)  
                - 'HTML': Use the HTML tag. (recommended for stimuli longer than 45s)
                - 'EXTERNAL': Use for externally hosted audio files. Web-audio api will be disabled            
            - ready_time: time before presentation of sound
            - timeout_after_playback: pause in ms after playback has finished
            - playhead: from where the audio file should play (offset in seconds from start)
            - mute: whether audio should be muted
            - auto_play: whether sound will start automatically
            - stop_audio_after: after how many seconds playback audio should be stopped
            - show_animation: whether to show an animation during playback 
            - (multiplayer) label_style: player index number style: NUMERIC, ALPHABETIC, ROMAN or empty (no label)
            - play_once: the sound can only be played once
            - resume_play: if the playback should resume from where a previous view left off
    '''

    TYPE_AUTOPLAY = 'AUTOPLAY'
    TYPE_BUTTON = 'BUTTON'
    TYPE_MULTIPLAYER = 'MULTIPLAYER'
    TYPE_SPECTROGRAM = 'SPECTROGRAM'

    def __init__(self, sections, player_type='AUTOPLAY', preload_message='', instruction='', play_config=None):
        self.sections = [{'id': s.id, 'url': s.absolute_url(), 'group': s.group}
                         for s in sections]
        self.ID = player_type
        self.preload_message = preload_message
        self.instruction = instruction
        self.play_config = {
            'play_method': 'BUFFER',
            'external_audio': False,
            'ready_time': 0,
            'playhead': 0,
            'show_animation': False,
            'mute': False,
            'play_once': False,
            'resume_play': False
        }
        if play_config:
            self.play_config.update(play_config)
