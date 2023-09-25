let track;
let source
let buffers = {};
let audioContext

export let audioInitialized = false;
    
// Play a silent mp3 to make the buffer play after a user action
// after that other audio can be started programmatically
// More info: https://developer.mozilla.org/en-US/docs/Web/Media/Autoplay_guide
export const init = () => {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
};

// init audio after first user action on page
export const initWebAudioListener = () => {
    const initOnce = () => {
        document.removeEventListener("click", initOnce);
        init();
    };
    document.addEventListener("click", initOnce);
};

// init HTML audio element in webaudio context and connect track to destination (output)
export const initWebAudio = () => {
    if (track === undefined) {                 
        track = audioContext.createMediaElementSource(window.audio);
        track.connect(audioContext.destination);        
    }
    return getTotalLatency();
}

// Change HTML audio element crossorigin attribute for playing external files
export const closeWebAudio = () => {
    window.audio.removeAttribute('crossOrigin');    
    window.audio.crossorigin = "use-credentials";    
}

// return total audio latency in milliseconds
export const getTotalLatency = () => {    
    let totalLatency = (audioContext.outputLatency + audioContext.baseLatency) * 1000;
    console.log(`Latency: ${totalLatency}ms`);
    return totalLatency;
}

// return base audio latency in seconds
export const getBaseLatency = () => {
    return audioContext.baseLatency;
}

// return output audio latency in seconds
export const getOutputLatency = () => {    
    return audioContext.outputLatency;
}

// Adjust gain
export const changeGain = (level) => {
    const gainNode = audioContext.createGain();
    track.connect(gainNode).connect(audioContext.destination);
    gainNode.gain.value = level;    
}

// load sound data and store in buffers object
export const loadBuffer = async (id, src, canPlay) => {    
    await fetch(src, {})
    // Return the data as an ArrayBuffer
        .then(response => response.arrayBuffer())
        // Decode the audio data
        .then(buffer => audioContext.decodeAudioData(buffer))
        // store buffer in buffers object
        .then(decodedData => {            
            buffers[id] = decodedData;
            console.log(buffers);
            canPlay();
        });
}

export const clearBuffers = () => {
    buffers = {};
}

// stop buffer playback
export const stopBuffer = () => {
    if (source) {
        source.stop();
    }    
}

// play buffer by section.id
export const playBuffer = (id) => {
    source = audioContext.createBufferSource();
    source.buffer = buffers[id]; // <==            
    source.connect(audioContext.destination);    
    source.start();
}
export const playBufferFrom = (id, time) => {
    source = audioContext.createBufferSource();
    source.buffer = buffers[id]; // <==            
    source.connect(audioContext.destination);    
    source.start(0, time);
}

// Suspend webaudio (frees up resources)
export const suspend = () => {
    audioContext.suspend();
}

// Resume webaudio
export const resume = () => {
    audioContext.resume();
}

// Listen once to the given event
// After that remove listener
export const listenOnce = (event, callback) => {
    const remove = () => {
        source.removeEventListener(event, _callback);
    };
    const _callback = () => {
        remove();
        callback();
    };
    source.addEventListener(event, _callback);
    return remove;
};