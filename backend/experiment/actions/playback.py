from typing import List, Optional, Any, Literal, TypedDict

from .base_action import BaseAction
from .button import Button
from section.validators import audio_extensions

from section.models import Section

# player types
TYPE_AUTOPLAY = "AUTOPLAY"
TYPE_BUTTON = "BUTTON"
TYPE_MATCHINGPAIRS = "MATCHINGPAIRS"

# playback methods
PLAY_EXTERNAL = "EXTERNAL"
PLAY_HTML = "HTML"
PLAY_BUFFER = "BUFFER"
PLAY_NOAUDIO = "NOAUDIO"

PlayMethods = Literal["EXTERNAL", "HTML", "BUFFER", "NOAUDIO"]


class PlaybackSectionAction(TypedDict):
    """This type is similar to the ButtonAction type, but here link is the only required argument."""

    link: str
    label: Optional[str]
    color: str
    play_from: float
    mute: bool
    play_method: PlayMethods


class PlaybackSection(Button):
    '''An object to represent a section to be played
    Args:
        link (str): Link to audio file
        label (Optional[str]): Label of play button (not shown in autoplay mode)
        color (Optional[str]): Color of play button (not shown in autoplay mode)
        play_from (float): Start position of the audio file in seconds
        mute (bool): Whether to mute this section

    Infers a playback method for this section, i.e., whether the frontend will use webAudio and whether it will buffer.
    Currently there is no support for mixed playback methods.
    '''

    def __init__(self, section: Section, label="", play_from=0, mute=False, **kwargs):
        super().__init__(label, **kwargs)
        self.play_from = play_from
        self.link = section.absolute_url()
        self.play_method = get_play_method(section)
        self.mute = mute


class SectionImage(TypedDict):
    link: str
    label: Optional[str]


class ImagePlaybackSectionAction(PlaybackSectionAction):
    image: SectionImage


class ImagePlaybackSection(PlaybackSection):
    """A special type of PlaybackSection that shows an image along a play button"""

    def __init__(self, image: SectionImage, **kwargs):
        super().__init__(**kwargs)
        self.image = image

    def action(self) -> ImagePlaybackSectionAction:
        serialized = super().action()
        serialized['image'] = self.image.__dict__
        return serialized


class Playback(BaseAction):
    """Base class for different kinds of audio players.

    Args:
        sections (List[PlaySection]): List of audio sections to play.
        preload_message (str): Text to display during preload. Defaults to "".
        instruction (str): Text to display during presentation. Defaults to "".
        show_animation (bool): Whether to show playback animation. Defaults to False.
        mute (bool): Whether to mute audio. Defaults to False.
        timeout_after_playback (Optional[float]): Seconds to wait after playback before proceeding. Defaults to None.
        stop_audio_after (Optional[float]): Seconds after which to stop playback. Defaults to None.
        resume_play (bool): Whether to resume from previous position. Defaults to False.
        show_animation (bool): Whether to show an animated histogram during playback (applies for AutoPlay & MatchingPairs)
        style (Optional[list[str]]): CSS class name(s) set in the frontend for styling
    """

    def __init__(
        self,
        sections: List[PlaybackSection],
        preload_message: str = "",
        instruction: str = "",
        resume_play: bool = False,
        show_animation: bool = True,
        style: Optional[list[str]] = None,
    ) -> None:
        self.sections = sections
        self.preload_message = preload_message
        self.instruction = instruction
        self.resume_play = resume_play
        self.show_animation = show_animation
        self.style = self._apply_style(style)

    def action(self):
        serialized = super().action()
        serialized['sections'] = [section.action() for section in self.sections]
        return serialized


class Autoplay(Playback):
    """Player that starts playing automatically.

    Args:
        sections List[AudioSection]: List of audio sections to play. Currently does not support more than one section.
        **kwargs: Additional arguments passed to `Playback`.

    Example:
        ```python
        Autoplay(
            sections=[PlaybackSection(section1)],
            show_animation=True,
        )
        ```

    Note:
        If show_animation is True, displays a countdown and moving histogram.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.view = TYPE_AUTOPLAY


class PlayButtons(Playback):
    """Player that shows buttons for each to trigger playback.

    Args:
        sections (List[Section]): List of audio sections to play.
        play_once: Whether button should be disabled after one play. Defaults to False.
        **kwargs: Additional arguments passed to Playback.

    Example:
        ```python
        PlayButtons(
            sections=[PlaybackSection(section1), PlaybackSection(section2)],
            play_once=False,
        )
        ```
    """

    def __init__(self, play_once: bool = False, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.view = TYPE_BUTTON
        self.play_once = play_once


ScoreFeedbackDisplay = Literal["small-bottom-right", "large-top", "hidden"]


class MatchingPairs(Playback):
    """Multiplayer where buttons are represented as cards and where the cards need to be matched based on audio.

    Args:
        sections (List[Section]): List of audio sections to play.
        show_animation (bool): Whether to show an animated histogram during playback of a card.
        score_feedback_display (ScoreFeedbackDisplay): How to display score feedback. Defaults to "large-top" (pick from "small-bottom-right", "large-top", "hidden").
        **kwargs: Additional arguments passed to Multiplayer.

    Example:
        ```python
        MatchingPairs(
            # You will need an even number of sections (ex. 16)
            [section1, section2, section3, section4, section5, section6, section7, section8, section9, section10, section11, section12, section13, section14, section15, section16],
            score_feedback_display="large-top",
         ```
    """

    def __init__(
        self,
        sections: List[Section],
        show_animation: bool = True,
        score_feedback_display: ScoreFeedbackDisplay = "large-top",
        **kwargs: Any,
    ) -> None:
        super().__init__(sections, **kwargs)
        self.view = TYPE_MATCHINGPAIRS
        self.show_animation = show_animation
        self.score_feedback_display = score_feedback_display


def get_play_method(section: Section) -> PlayMethods:
    """Determine which play method to use based on section properties.

    Args:
        section (Section): Audio section object.

    Returns:
        str: Play method constant (PLAY_NOAUDIO, PLAY_EXTERNAL, PLAY_HTML, or PLAY_BUFFER).
    """
    filename = str(section.filename)
    if not is_audio_file(filename):
        return PLAY_NOAUDIO
    elif filename.startswith("http"):
        return PLAY_EXTERNAL
    elif section.duration > 45:
        return PLAY_HTML
    else:
        return PLAY_BUFFER


def is_audio_file(filename: str) -> bool:
    """Check if filename has an audio extension.

    Args:
        filename (str): Name of the file to check.

    Returns:
        bool: True if file has an audio extension.
    """
    return any(filename.lower().endswith(ext) for ext in audio_extensions)
