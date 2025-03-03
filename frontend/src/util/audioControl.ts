import Section from "@/types/Section";
import * as audio from "./audio";
import * as webAudio from "./webAudio";
import { PlaybackArgs } from "@/types/Playback";

export const playAudio = (section: Section, playMethod: PlaybackArgs['play_method'], playheadShift = 0) => {
    let latency = 0;

    if (playMethod === 'BUFFER') {

        // Determine latency for current audio device
        latency = webAudio.getTotalLatency();
        window.sessionStorage.setItem('audioLatency', latency);
        // Play audio
        webAudio.playBufferFrom(section.id.toString(), playheadShift);

        return latency
    } else {

        // Only initialize webaudio if section is hosted local
        if (playMethod !== 'EXTERNAL') {
            // Determine latency for current audio device
            latency = webAudio.getTotalLatency();
            window.sessionStorage.setItem('audioLatency', latency);
            webAudio.initWebAudio();
        }

        // Volume 1
        audio.setVolume(1);

        // Play audio
        audio.loadUntilAvailable(section.url, () => {
            audio.playFrom(Math.max(0, playheadShift));
        });

        return latency
    }
}

export const pauseAudio = (playMethod: PlaybackArgs['play_method']) => {
    if (playMethod === 'BUFFER') {
        webAudio.stopBuffer();
    } else {
        audio.stop();
    }
}
