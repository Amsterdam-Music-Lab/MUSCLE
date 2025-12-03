interface PlaybackImage {
    link: string,
    label: string
}

type PlaybackMethod = "EXTERNAL" | "HTML" | "BUFFER" | "NOAUDIO";

export interface PlaybackSection {
    link: string,
    label: string,
    color?: string,
    image: PlaybackImage,
    playFrom: number,
    playMethod: PlaybackMethod,
    mute: boolean,
    playing: boolean,
    hasPlayed: boolean
}

export interface Card extends PlaybackSection {
    name: string;
    turned: boolean;
    inactive: boolean;
    matchClass: string;
    seen: boolean;
    noevents: boolean;
    boardposition: number;
    timestamp: number;
    response_interval_ms: number | string;
    audio_latency_ms?: number;
}

export default PlaybackSection;
