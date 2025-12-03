interface PlaybackImage {
    link: string,
    label: string
}

export interface PlaybackSection {
    link: string,
    label: string,
    color?: string,
    image: PlaybackImage,
    play_from: number,
    mute: boolean
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

export default Section;
