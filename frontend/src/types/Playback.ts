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
    root: string | FrontendStyle;
    [key: string]: string | FrontendStyle;
}

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
    score_feedback_display?: string;
    tutorial?: { [key: string]: string };
}
