from .base_action import BaseAction

# player types
TYPE_AUTOPLAY = 'AUTOPLAY'
TYPE_BUTTON = 'BUTTON'
TYPE_IMAGE = 'IMAGE'
TYPE_MULTIPLAYER = 'MULTIPLAYER'
TYPE_MATCHINGPAIRS = 'MATCHINGPAIRS'

# playback methods
PLAY_EXTERNAL = 'EXTERNAL'
PLAY_HTML = 'HTML'
PLAY_BUFFER = 'BUFFER'

# labeling
allowed_player_label_styles = ['ALPHABETIC', 'NUMERIC', 'ROMAN']

class Playback(BaseAction):
    ''' A playback wrapper for different kinds of players
        - view: can be one of the following:
            - 'AUTOPLAY' - player starts automatically
            - 'BUTTON' - display one play button
            - 'MULTIPLAYER' - display multiple small play buttons, one per section
            - 'IMAGE' - extends multiplayer with a list of spectrograms
        - sections: a list of sections (in many cases, will only contain *one* section)
        - preload_message: text to display during preload
        - instruction: text to display during presentation of the sound
        - play_from: from where in the file to start playback. Set to None to mute
        - ready_time: how long to countdown before playback
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
    '''

    def __init__(self,
                 sections,
                 preload_message='',
                 instruction='',
                 play_from=0,
                 ready_time=0,
                 timeout_after_playback=None):
        self.sections = [{'id': s.id, 'url': s.absolute_url(), 'group': s.group}
                         for s in sections]
        if not sections[0].absolute_url().startswith('server'):
            self.play_method = PLAY_EXTERNAL
        elif sections[0].duration > 44.9:
            self.play_method = PLAY_HTML
        else:
            self.play_method = PLAY_BUFFER
        self.preload_message = preload_message
        self.instruction = instruction
        self.play_from = play_from
        self.ready_time = ready_time
        self.timeout_after_playback = timeout_after_playback
        # self.play_config = {
        #     'play_method': 'BUFFER',
        #     'external_audio': False,
        #     'ready_time': 0,
        #     'playhead': 0,
        #     'show_animation': False,
        #     'mute': False,
        #     'play_once': False,
        # }
        # if play_config:
        #     self.play_config.update(play_config)
    
class Autoplay(Playback):
    '''
    This player starts playing automatically
    - show_animation: if True, show a countdown and moving histogram
    '''
    def __init__(self, sections, show_animation=False, **kwargs):
        super().__init__(sections, **kwargs)
        self.show_animation = show_animation        
        self.ID = TYPE_AUTOPLAY
    

class PlayButton(Playback):
    '''
    This player shows a button, which triggers playback
    - play_once: if True, button will be disabled after one play
    '''
    def __init__(self, sections, play_once=False, **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_BUTTON
        self.play_once = play_once

class Multiplayer(PlayButton):
    '''
    This is a player with multiple play buttons
    - stop_audio_after: after how many seconds to stop audio
    - label_style: set if players should be labeled in alphabetic / numeric  / roman style (based on player index)
    - labels: pass list of strings if players should have custom labels
    '''
    def __init__(self, sections, stop_audio_after=5, label_style='', labels=[], **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_MULTIPLAYER
        self.stop_audio_after = stop_audio_after
        if label_style:
            if label_style not in allowed_player_label_styles:
                raise UserWarning('Unknown label style: choose alphabetic, numeric or roman ordering')
            self.label_stye = label_style
        if labels:
            if len(labels) != len(self.sections):
                raise UserWarning('Number of labels and sections for the play buttons do not match')
            self.labels = labels
            self.label_stye = label_style

class ImagePlayer(PlayButton):
    '''
    This is a special case of the Multiplayer:
    it shows an image next to each play button
    '''
    def __init__(self, sections, images, image_labels=[], **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_IMAGE
        if len(images) != len(self.sections):
            raise UserWarning('Number of images and sections for the ImagePlayer do not match')
        self.images = images
        if image_labels:
            if len(image_labels) != len(self.sections):
                raise UserWarning('Number of image labels and sections do not match')
            self.image_labels = image_labels
    
class MatchingPairs(Multiplayer):
    '''
    This is a special case of multiplayer:
    play buttons are represented as cards
    '''
    def __init__(self, sections, **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_MATCHINGPAIRS