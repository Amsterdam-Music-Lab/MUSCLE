import * as audio from "./audio";
import * as webAudio from "./webAudio";

export const playAudio = (section, playMethod, playheadShift=0) => {
    let latency = 0;
    const playhead = playConfig.playhead + playheadShift

    if (playMethod === 'BUFFER') {
        
        // Determine latency for current audio device
        latency = webAudio.getTotalLatency()
        // Play audio
        webAudio.playBufferFrom(section.id, playhead);

        return latency
    } else {        

        // Only initialize webaudio if section is hosted local
        if (playMethod !== 'EXTERNAL') {
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

export const pauseAudio = (playMethod) => {
    if (playMethod === 'BUFFER') {
        webAudio.stopBuffer();
    } else {
        audio.stop();
    }    
}
