import PlaybackSection from "./Section";

export const AUTOPLAY = "AUTOPLAY";
export const BUTTON = "BUTTON";
export const MULTIPLAYER = "MULTIPLAYER";
export const IMAGE = "IMAGE";
export const MATCHINGPAIRS = "MATCHINGPAIRS";
export const PRELOAD = "PRELOAD";

export type PlaybackView = typeof AUTOPLAY | typeof BUTTON | typeof MULTIPLAYER | typeof IMAGE | typeof MATCHINGPAIRS | typeof PRELOAD;

export type ScoreFeedbackDisplay = "large-top" | "small-bottom-right" | "hidden";

// the information received from the backend
export interface PlaybackAction {
    view: PlaybackView;
    showAnimation: boolean;
    preloadMessage: string;
    instruction: string;
    sections: PlaybackSection[];
    mute: boolean;
    resumePlay?: boolean;
    playOnce?: boolean;
    scoreFeedbackDisplay?: ScoreFeedbackDisplay;
}
