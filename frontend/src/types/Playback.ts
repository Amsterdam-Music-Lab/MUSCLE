import Section from "./Section";

export const AUTOPLAY = "AUTOPLAY";
export const BUTTON = "BUTTON";
export const MULTIPLAYER = "MULTIPLAYER";
export const IMAGE = "IMAGE";
export const MATCHINGPAIRS = "MATCHINGPAIRS";
export const PRELOAD = "PRELOAD";

export type PlaybackView = typeof AUTOPLAY | typeof BUTTON | typeof MULTIPLAYER | typeof IMAGE | typeof MATCHINGPAIRS | typeof PRELOAD;

type PlaybackMethod = "EXTERNAL" | "HTML" | "BUFFER" | "NOAUDIO";

interface FrontendStyle {
    [key: string]: boolean;
}

export type ScoreFeedbackDisplay = "large-top" | "small-bottom-right" | "hidden";

export interface PlaybackArgs {
    view: PlaybackView;
    play_method: PlaybackMethod;
    show_animation: boolean;
    preload_message: string;
    instruction: string;
    sections: Section[];
    play_from: number;

    labels?: string[];
    image_labels?: string[];
    images?: string[];
    style?: FrontendStyle;
    mute?: boolean;
    play_once?: boolean;
    resume_play?: boolean;
    stop_audio_after?: number;
    timeout_after_playback?: number;
    score_feedback_display?: ScoreFeedbackDisplay;
    tutorial?: { [key: string]: string };
}
