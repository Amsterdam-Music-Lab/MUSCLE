from typing import List, Dict, Optional, Any, Literal, TypedDict

from .base_action import BaseAction
from section.validators import audio_extensions

from section.models import Section

# player types
TYPE_AUTOPLAY = "AUTOPLAY"
TYPE_BUTTON = "BUTTON"
TYPE_IMAGE = "IMAGE"
TYPE_MULTIPLAYER = "MULTIPLAYER"
TYPE_MATCHINGPAIRS = "MATCHINGPAIRS"

# playback methods
PLAY_EXTERNAL = "EXTERNAL"
PLAY_HTML = "HTML"
PLAY_BUFFER = "BUFFER"
PLAY_NOAUDIO = "NOAUDIO"

PlayMethods = Literal["EXTERNAL", "HTML", "BUFFER", "NOAUDIO"]


class PlaybackSection(TypedDict):
    id: int
    url: str

    # TODO: Remove group from PlaybackSection and from the Playback class itself and make sure everything still works (see also https://github.com/Amsterdam-Music-Lab/MUSCLE/pull/1448#discussion_r1903978068)
    group: str


class Playback(BaseAction):
    """Base class for different kinds of audio players.

    Args:
        sections (List[Section]): List of audio sections to play.
        preload_message (str): Text to display during preload. Defaults to "".
        instruction (str): Text to display during presentation. Defaults to "".
        play_from (float): Start position in seconds. Defaults to 0.
        show_animation (bool): Whether to show playback animation. Defaults to False.
        mute (bool): Whether to mute audio. Defaults to False.
        timeout_after_playback (Optional[float]): Seconds to wait after playback before proceeding. Defaults to None.
        stop_audio_after (Optional[float]): Seconds after which to stop playback. Defaults to None.
        resume_play (bool): Whether to resume from previous position. Defaults to False.
        style (Optional[list[str]]): CSS class name(s) set in the frontend for styling
        tutorial (Optional[Dict[str, Any]]): Tutorial configuration dictionary. Defaults to None.
    """

    sections: List[PlaybackSection]

    def __init__(
        self,
        sections: List[Section],
        preload_message: str = "",
        instruction: str = "",
        play_from: float = 0,
        show_animation: bool = False,
        mute: bool = False,
        timeout_after_playback: Optional[float] = None,
        stop_audio_after: Optional[float] = None,
        resume_play: bool = False,
        style: Optional[list[str]] = None,
        tutorial: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.sections = [{"id": s.id, "url": s.absolute_url(), "group": s.group} for s in sections]
        self.play_method = determine_play_method(sections[0])
        self.show_animation = show_animation
        self.preload_message = preload_message
        self.instruction = instruction
        self.play_from = play_from
        self.mute = mute
        self.timeout_after_playback = timeout_after_playback
        self.stop_audio_after = stop_audio_after
        self.resume_play = resume_play
        self.style = self._apply_style(style)
        self.tutorial = tutorial


class Autoplay(Playback):
    """Player that starts playing automatically.

    Args:
        sections List[Section]: List of audio sections to play.
        **kwargs: Additional arguments passed to `Playback`.

    Example:
        ```python
        Autoplay(
            [section1, section2],
            show_animation=True,
        )
        ```

    Note:
        If show_animation is True, displays a countdown and moving histogram.
    """

    def __init__(self, sections: List[Section], **kwargs: Any) -> None:
        super().__init__(sections, **kwargs)
        self.view = TYPE_AUTOPLAY


class PlayButton(Playback):
    """Player that shows a button to trigger playback.

    Args:
        sections (List[Section]): List of audio sections to play.
        play_once: Whether button should be disabled after one play. Defaults to False.
        **kwargs: Additional arguments passed to Playback.

    Example:
        ```python
        PlayButton(
            [section1, section2],
            play_once=False,
        )
        ```
    """

    def __init__(self, sections: List[Section], play_once: bool = False, **kwargs: Any) -> None:
        super().__init__(sections, **kwargs)
        self.view = TYPE_BUTTON
        self.play_once = play_once


class Multiplayer(PlayButton):
    """Player with multiple play buttons.

    Args:
        sections (List[Section]): List of audio sections to play.
        stop_audio_after (float): Seconds after which to stop audio. Defaults to 5.
        labels (List[str]): Custom labels for players. Defaults to empty list.
        style (FrontendStyle): Frontend styling options.
        **kwargs: Additional arguments passed to PlayButton.

    Example:
        ```python
        Multiplayer(
            [section1, section2],
            stop_audio_after=3,
            labels=["Play 1", "Play 2"],
        )
        ```

    Raises:
        UserWarning: If `labels` is defined, and number of labels doesn't match number of sections.
    """

    def __init__(
        self,
        sections: List[Section],
        stop_audio_after: float = 5,
        labels: List[str] = [],
        style: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(sections, **kwargs)
        self.view = TYPE_MULTIPLAYER
        self.stop_audio_after = stop_audio_after
        self.style = self._apply_style(style)
        if labels:
            if len(labels) != len(self.sections):
                raise UserWarning("Number of labels and sections for the play buttons do not match")
            self.labels = labels


class ImagePlayer(Multiplayer):
    """Multiplayer that shows an image next to each play button.

    Args:
        sections (List[Section]): List of audio sections to play.
        images (List[str]): List of image paths/urls to display.
        image_labels (List[str]): Optional labels for images. Defaults to empty list.
        **kwargs: Additional arguments passed to Multiplayer.

    Example:
        ```python
        ImagePlayer(
            [section1, section2],
            images=["image1.jpg", "image2.jpg"],
            image_labels=["Image 1", "Image 2"],
        )
        ```

    Raises:
        UserWarning: If number of images or labels doesn't match sections.
    """

    def __init__(
        self,
        sections: List[Section],
        images: List[str],
        image_labels: List[str] = [],
        **kwargs: Any,
    ) -> None:
        super().__init__(sections, **kwargs)
        self.view = TYPE_IMAGE
        if len(images) != len(self.sections):
            raise UserWarning("Number of images and sections for the ImagePlayer do not match")
        self.images = images
        if image_labels:
            if len(image_labels) != len(self.sections):
                raise UserWarning("Number of image labels and sections do not match")
            self.image_labels = image_labels


ScoreFeedbackDisplay = Literal["small-bottom-right", "large-top", "hidden"]


class MatchingPairs(Multiplayer):
    """Multiplayer where buttons are represented as cards and where the cards need to be matched based on audio.

    Args:
        sections (List[Section]): List of audio sections to play.
        score_feedback_display (ScoreFeedbackDisplay): How to display score feedback. Defaults to "large-top" (pick from "small-bottom-right", "large-top", "hidden").
        tutorial (Optional[Dict[str, Any]]): Tutorial configuration dictionary. Defaults to None.
        **kwargs: Additional arguments passed to Multiplayer.

    Example:
        ```python
        MatchingPairs(
            # You will need an even number of sections (ex. 16)
            [section1, section2, section3, section4, section5, section6, section7, section8, section9, section10, section11, section12, section13, section14, section15, section16],
            score_feedback_display="large-top",
            tutorial={
                "no_match": _(
                    "This was not a match, so you get 0 points. Please try again to see if you can find a matching pair."
                ),
                "lucky_match": _(
                    "You got a matching pair, but you didn't hear both cards before. This is considered a lucky match. You get 10 points."
                ),
                "memory_match": _("You got a matching pair. You get 20 points."),
                "misremembered": _(
                    "You thought you found a matching pair, but you didn't. This is considered a misremembered pair. You lose 10 points."
                ),
            }
        )
        ```
    """

    def __init__(
        self,
        sections: List[Section],
        score_feedback_display: ScoreFeedbackDisplay = "large-top",
        tutorial: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(sections, **kwargs)
        self.view = TYPE_MATCHINGPAIRS
        self.score_feedback_display = score_feedback_display
        self.tutorial = tutorial


def determine_play_method(section: Section) -> PlayMethods:
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
