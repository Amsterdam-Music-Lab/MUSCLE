import Section from "@/types/Section";

let track: MediaElementAudioSourceNode;
let source: AudioBufferSourceNode;
let buffers: { [key: string]: AudioBuffer } = {};
let audioContext: AudioContext;
let analyzer: AnalyserNode;

export let audioInitialized = false;

// Declare audio property on window object
declare global {
    interface Window {
        audio: HTMLAudioElement;
        webkitAudioContext?: typeof AudioContext;
        audioContext: AudioContext;
        analyzer: AnalyserNode;
    }
}

// Create the AudioContext object after a user action
// after that other audio can be started programmatically
// More info: https://developer.mozilla.org/en-US/docs/Web/Media/Autoplay_guide
export const init = () => {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyzer = audioContext.createAnalyser();
    analyzer.fftSize = 32;
    window.audioContext = audioContext;
    window.analyzer = analyzer;
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
};

// Change HTML audio element crossorigin attribute for playing external files
export const closeWebAudio = () => {
    window.audio.removeAttribute('crossOrigin');
    window.audio.crossorigin = "use-credentials";
};

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
};

// return base audio latency in seconds
export const getBaseLatency = () => {
    return audioContext.baseLatency;
};

// return output audio latency in seconds
export const getOutputLatency = () => {
    return audioContext.outputLatency;
};

// Adjust gain
export const changeGain = (level: number) => {
    const gainNode = audioContext.createGain();
    track.connect(gainNode).connect(audioContext.destination);
    gainNode.gain.value = level;
};

// load sound data and store in buffers object
export const loadBuffer = async (link: string, canPlay: () => void) => {
    await fetch(link, {})
        // Return the data as an ArrayBuffer
        .then(response => response.arrayBuffer())
        // Decode the audio data
        .then(buffer => audioContext.decodeAudioData(buffer))
        // store buffer in buffers object
        .then(decodedData => {
            buffers[link] = decodedData;
            canPlay();
        });
};

export const checkSectionLoaded = (section: Section) => {
    if (buffers.hasOwnProperty(section.link)) {
        return true;
    };
};

// Clear buffer list
export const clearBuffers = () => {
    buffers = {};
};

// stop buffer playback
export const stopBuffer = () => {
    if (source) {
        source.stop();
    };
};

// Play buffer from given time
export const playBufferFrom = (id: string, time: number) => {
    source = audioContext.createBufferSource();
    source.buffer = buffers[id];
    source.connect(analyzer);
    analyzer.connect(audioContext.destination);
    source.start(0, time);
};

// Suspend webaudio (frees up resources)
export const suspend = () => {
    audioContext.suspend();
};

// Resume webaudio
export const resume = () => {
    audioContext.resume();
};

// Listen once to the given event
// After that remove listener
export const listenOnce = (event: string, callback: () => void) => {
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

// function to check wether a users device is webaudio compatible
export const compatibleDevice = () => {
    const userAgentString = window.navigator.userAgent;
    let compatible = true;
    // Disable webaudio for ios versions below 17
    if ((userAgentString.indexOf('iPhone') > -1 || userAgentString.indexOf('iPad') > -1) && (userAgentString.indexOf('OS') > -1)) {
        const iosVersion = userAgentString
            .substring(userAgentString
                .indexOf('OS') + 3, userAgentString
                    .indexOf('OS') + 5)

        const iosVersionInt = parseInt(iosVersion);

        if (iosVersionInt < 17) {
            compatible = false;
        }
    }
    return compatible;
};
