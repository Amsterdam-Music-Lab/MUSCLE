import { MEDIA_ROOT } from "../config";

let track;
let source;
let buffers = {};
let audioContext;
let previousSource;

export let audioInitialized = false;
    
// Create the AudioContext object after a user action
// after that other audio can be started programmatically
// More info: https://developer.mozilla.org/en-US/docs/Web/Media/Autoplay_guide
export const init = () => {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
};

// init webaudio after first user action on page
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
}

// Change HTML audio element crossorigin attribute for playing external files
export const closeWebAudio = () => {    
    window.audio.removeAttribute('crossOrigin');    
    window.audio.crossorigin = "use-credentials";    
}

// return total audio latency in milliseconds
export const getTotalLatency = () => {    
    let baseLatency = audioContext.baseLatency;
    let outputLatency = audioContext.outputLatency;

    // Check if the response is a valid number 
    if (isNaN(baseLatency)) {
        baseLatency = 0;
    }
    if (isNaN(outputLatency)) {
        outputLatency = 0;
    }
    
    let totalLatency = (baseLatency + outputLatency) * 1000;    
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
    await fetch(MEDIA_ROOT + src, {})
    // Return the data as an ArrayBuffer
        .then(response => response.arrayBuffer())
        // Decode the audio data
        .then(buffer => audioContext.decodeAudioData(buffer))
        // store buffer in buffers object
        .then(decodedData => {            
            buffers[id] = decodedData;
            previousSource = src;
            canPlay();
        });
}

export const checkSectionLoaded = (section) => {
    if (section.url === previousSource) {
        return true;
    }
} 

// Clear buffer list
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
    // temporary solution for ios17
    // https://devcodef1.com/news/1068842/fixing-ios-17-web-audio-issue
    audioContext.close();
    audioContext = new (window.AudioContext || window.webkitAudioContext)();

    source = audioContext.createBufferSource();
    source.buffer = buffers[id];
    source.connect(audioContext.destination);    
    source.start();
}

// Play buffer from given time
export const playBufferFrom = (id, time) => {
    // temporary solution for ios17
    // https://devcodef1.com/news/1068842/fixing-ios-17-web-audio-issue
    audioContext.close();
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    
    source = audioContext.createBufferSource();
    source.buffer = buffers[id];          
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
