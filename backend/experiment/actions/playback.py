from typing import List, Dict

from .base_action import BaseAction

# player types
TYPE_AUTOPLAY = 'AUTOPLAY'
TYPE_BUTTON = 'BUTTON'
TYPE_IMAGE = 'IMAGE'
TYPE_MULTIPLAYER = 'MULTIPLAYER'
TYPE_MATCHINGPAIRS = 'MATCHINGPAIRS'
TYPE_VISUALMATCHINGPAIRS = 'VISUALMATCHINGPAIRS'

# playback methods
PLAY_EXTERNAL = 'EXTERNAL'
PLAY_HTML = 'HTML'
PLAY_BUFFER = 'BUFFER'
PLAY_NOAUDIO = 'NOAUDIO'


class Playback(BaseAction):
    ''' A playback base class for different kinds of players
        - sections: a list of sections (in many cases, will only contain *one* section)
        - preload_message: text to display during preload
        - instruction: text to display during presentation of the sound
        - play_from: where in the audio file to start playing/
        - ready_time: how long to show the "Preload" view (loading spinner)
        - show_animation: whether to show animations with this player
        - mute: whether to mute the audio
        - timeout_after_playback: once playback has finished, add optional timeout (in seconds) before proceeding
        - stop_audio_after: stop playback after so many seconds
        - resume_play: if the playback should resume from where a previous view left off
    '''

    def __init__(self,
                 sections,
                 preload_message='',
                 instruction='',
                 play_from=0,
                 ready_time=0,
                 show_animation=False,
                 mute=False,
                 timeout_after_playback=None,
                 stop_audio_after=None,
                 resume_play=False):
        self.sections = [{'id': s.id, 'url': s.absolute_url(), 'group': s.group}
                         for s in sections]
        if str(sections[0].filename).startswith('http'):
            self.play_method = PLAY_EXTERNAL
        elif sections[0].duration > 45:
            self.play_method = PLAY_HTML
        else:
            self.play_method = PLAY_BUFFER
        self.show_animation = show_animation
        self.preload_message = preload_message
        self.instruction = instruction
        self.play_from = play_from
        self.mute = mute
        self.ready_time = ready_time
        self.timeout_after_playback = timeout_after_playback
        self.stop_audio_after = stop_audio_after
        self.resume_play = resume_play


class Autoplay(Playback):
    '''
    This player starts playing automatically
    - show_animation: if True, show a countdown and moving histogram
    '''

    def __init__(self, sections, **kwargs):
        super().__init__(sections, **kwargs)
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

    def __init__(self, sections, stop_audio_after=5, labels=[], **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_MULTIPLAYER
        self.stop_audio_after = stop_audio_after
        if labels:
            if len(labels) != len(self.sections):
                raise UserWarning(
                    'Number of labels and sections for the play buttons do not match')
            self.labels = labels


class ImagePlayer(PlayButton):
    '''
    This is a special case of the Multiplayer:
    it shows an image next to each play button
    '''

    def __init__(self, sections, images, image_labels=[], **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_IMAGE
        if len(images) != len(self.sections):
            raise UserWarning(
                'Number of images and sections for the ImagePlayer do not match')
        self.images = images
        if image_labels:
            if len(image_labels) != len(self.sections):
                raise UserWarning(
                    'Number of image labels and sections do not match')
            self.image_labels = image_labels


class MatchingPairs(Multiplayer):
    '''
    This is a special case of multiplayer:
    play buttons are represented as cards
    '''

    def __init__(self, sections: List[Dict], display_score: str = 'large_top', **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_MATCHINGPAIRS
        self.display_score = display_score


class VisualMatchingPairs(MatchingPairs):
    '''
    This is a special case of multiplayer:
    play buttons are represented as cards
    this player does not play audio, but displays images instead
    '''

    def __init__(self, sections, **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_VISUALMATCHINGPAIRS
        self.play_method = PLAY_NOAUDIO
