export interface Section {
    id: number;
    url: string;
}

export interface Card extends Section {
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
