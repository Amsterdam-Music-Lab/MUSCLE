let audioContext;
let track;

// init audio in webaudio context and connect track to destination (output)
export const initWebAudio = () => {
    if (track === undefined) {
        audioContext = new AudioContext();
        track = audioContext.createMediaElementSource(window.audio);
        track.connect(audioContext.destination);        
    }
}

// return total audio latency in milliseconds
export const getTotalLatency = () => {    
    let totalLatency = (track === undefined) ? 0 : (audioContext.outputLatency + audioContext.baseLatency) * 1000;    
    console.log(`Compensated ${totalLatency}ms (Base:${audioContext.baseLatency * 1000}ms + Output:${audioContext.outputLatency * 1000}ms)`);    
    return totalLatency
}

// return base audio latency in seconds
export const getBaseLatency = () => {
    return audioContext.baseLatency
}

// return output audio latency in seconds
export const getOutputLatency = () => {    
    return audioContext.outputLatency
}

// Adjust gain
export const changeGain = (level) => {
    const gainNode = audioContext.createGain();
    track.connect(gainNode).connect(audioContext.destination);
    gainNode.gain.value = level;    
}