import * as audio from "./audio";
import * as webAudio from "./webAudio";

export const playAudio = (playConfig, section) => {    
    let latency = 0;

    if (playConfig.play_method === 'BUFFER') {
        
        // Determine latency for current audio device
        latency = webAudio.getTotalLatency()
        // Play audio
        webAudio.playBufferFrom(section.id, Math.max(0, playConfig.playhead || 0));

        return latency
    } else {        

        // Only initialize webaudio if section is hosted local
        if (playConfig.play_method !== 'EXTERNAL') {
            // Determine latency for current audio device
            latency = webAudio.getTotalLatency()
            webAudio.initWebAudio();            
        }

        // Volume 1
        audio.setVolume(1);

        // Play audio
        audio.playFrom(Math.max(0, playConfig.playhead || 0));
        
        return latency
    }
}

export const pauseAudio = (playConfig) => {
    if (playConfig.play_method === 'BUFFER') {
        webAudio.stopBuffer();
    } else {
        audio.stop();
    }    
}
