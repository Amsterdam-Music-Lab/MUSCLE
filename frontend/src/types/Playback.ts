export const AUTOPLAY = "AUTOPLAY";
export const BUTTON = "BUTTON";
export const MULTIPLAYER = "MULTIPLAYER";
export const IMAGE = "IMAGE";
export const MATCHINGPAIRS = "MATCHINGPAIRS";
export const PRELOAD = "PRELOAD";

export type PlaybackView = typeof AUTOPLAY | typeof BUTTON | typeof MULTIPLAYER | typeof IMAGE | typeof MATCHINGPAIRS | typeof PRELOAD;

type PlaybackMethod = "EXTERNAL" | "HTML" | "BUFFER" | "NOAUDIO";

export interface PlaybackArgs {
    view: PlaybackView;
    play_method: PlaybackMethod;
    mute: boolean;
    play_once: boolean;
    resume_play: boolean;
    show_animation: boolean;
    timeout_after_playback: number;
    preload_message: string;
    instruction: string;
    labels: { [key: string]: string };
    images: { [key: string]: string };
    sections: any[];
    style: any;
    stop_audio_after: number;
    play_from: number;
    score_feedback_display: string;
}
