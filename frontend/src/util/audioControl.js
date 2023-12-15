import * as audio from "./audio";
import * as webAudio from "./webAudio";

export const playAudio = (playConfig, section, playheadShift=0) => {    
    let latency = 0;
    const playhead = playConfig.playhead + playheadShift

    if (playConfig.play_method === 'BUFFER') {
        
        // Determine latency for current audio device
        latency = webAudio.getTotalLatency()
        // Play audio
        webAudio.playBufferFrom(section.id, playhead);

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
        audio.playFrom(Math.max(0, playhead));
        
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
