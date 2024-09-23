from typing import List, Dict

from .frontend_style import FrontendStyle
from .base_action import BaseAction
from section.validators import audio_extensions

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
PLAY_NOAUDIO = 'NOAUDIO'


class Playback(BaseAction):
    ''' A playback base class for different kinds of players
        - sections: a list of sections (in many cases, will only contain *one* section)
        - preload_message: text to display during preload
        - instruction: text to display during presentation of the sound
        - play_from: where in the audio file to start playing/
        - show_animation: whether to show animations with this player
        - mute: whether to mute the audio
        - timeout_after_playback: once playback has finished, add optional timeout (in seconds) before proceeding
        - stop_audio_after: stop playback after so many seconds
        - resume_play: if the playback should resume from where a previous view left off
    '''

    def __init__(
        self,
        sections,
        preload_message='',
        instruction='',
        play_from=0,
        show_animation=False,
        mute=False,
        timeout_after_playback=None,
        stop_audio_after=None,
        resume_play=False,
        style=FrontendStyle()
    ):
        self.sections = [{'id': s.id, 'url': s.absolute_url(), 'group': s.group}
                         for s in sections]
        self.play_method = determine_play_method(sections[0])
        self.show_animation = show_animation
        self.preload_message = preload_message
        self.instruction = instruction
        self.play_from = play_from
        self.mute = mute
        self.timeout_after_playback = timeout_after_playback
        self.stop_audio_after = stop_audio_after
        self.resume_play = resume_play
        self.style = style


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
    - labels: pass list of strings if players should have custom labels
    '''

    def __init__(
        self,
        sections,
        stop_audio_after=5,
        labels=[],
        style=FrontendStyle(),
        **kwargs,
    ):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_MULTIPLAYER
        self.stop_audio_after = stop_audio_after
        self.style = style
        if labels:
            if len(labels) != len(self.sections):
                raise UserWarning(
                    'Number of labels and sections for the play buttons do not match')
            self.labels = labels


class ImagePlayer(Multiplayer):
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
    - sections: a list of sections (in many cases, will only contain *one* section)
    - score_feedback_display: how to display the score feedback (large-top, small-bottom-right, hidden)
    '''

    def __init__(self, sections: List[Dict], score_feedback_display: str = 'large-top', **kwargs):
        super().__init__(sections, **kwargs)
        self.ID = TYPE_MATCHINGPAIRS
        self.score_feedback_display = score_feedback_display


def determine_play_method(section):
    filename = str(section.filename)
    if not is_audio_file(filename):
        return PLAY_NOAUDIO
    elif filename.startswith('http'):
        return PLAY_EXTERNAL
    elif section.duration > 45:
        return PLAY_HTML
    else:
        return PLAY_BUFFER


def is_audio_file(filename):
    return any(filename.lower().endswith(ext) for ext in audio_extensions)
