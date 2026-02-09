import Section from "@/types/Section";
import * as audio from "./audio";
import * as webAudio from "./webAudio";

export const playAudio = (section: Section, playMethod: string, playheadShift = 0) => {
    let latency = 0;

    if (playMethod === 'BUFFER') {

        // Determine latency for current audio device
        latency = webAudio.getTotalLatency();
        window.sessionStorage.setItem('audioLatency', latency.toString());
        // Play audio
        webAudio.playBufferFrom(section.link, playheadShift);

        return latency
    } else {

        // Only initialize webaudio if section is hosted local
        if (playMethod !== 'EXTERNAL') {
            // Determine latency for current audio device
            latency = webAudio.getTotalLatency();
            window.sessionStorage.setItem('audioLatency', latency.toString());
            webAudio.initWebAudio();
        }

        // Volume 1
        audio.setVolume(1);

        // Play audio
        audio.loadUntilAvailable(section.link, () => {
            audio.playFrom(Math.max(0, playheadShift));
        });

        return latency
    }
}

export const pauseAudio = (playMethod: string) => {
    if (playMethod === 'BUFFER') {
        webAudio.stopBuffer();
    } else {
        audio.stop();
    }
}
