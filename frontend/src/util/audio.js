import { API_ROOT, SILENT_MP3 } from "../config.js";
import Timer from "./timer";

// Audio provides function around a shared audio object
// Create a global audio object once
// <audio /> docs: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio
const audio = document.createElement("audio");
audio.id = "audio-player";
audio.controls = "controls";
audio.src = SILENT_MP3;
audio.setAttribute('crossOrigin', 'use-credentials');
audio.disableRemotePlayback = true;
audio.style.display = "none";

// Required for Firefox to trigger canplaythrough event
audio.preload = "auto";

// Required for Safari/iOS
audio.load();

// Add it to the page
document.body.appendChild(audio);

// expose global
window.audio = audio;

let _stopFadeTimer = null;
export let audioInitialized = false;

// Play a silent mp3 to make the audio element play after a user action
// after that other audio can be started programmatically
// More info: https://developer.mozilla.org/en-US/docs/Web/Media/Autoplay_guide
export const init = () => {
    load(SILENT_MP3);
    play();
    audioInitialized = true;   
};

// init audio after first user action on page
export const initAudioListener = () => {
    const initOnce = () => {
        document.removeEventListener("click", initOnce);
        init();
    };
    document.addEventListener("click", initOnce);
};

export const stopFadeTimer = () => {
    if (_stopFadeTimer) {
        _stopFadeTimer();
    }
    _stopFadeTimer = null;
};

// Fade in volume
export const fadeIn = (duration = 0.1) => {
    if (_stopFadeTimer) {
        stopFadeTimer();
    }
    _stopFadeTimer = Timer({
        duration,
        onTick: (_, delta) => {
            let v = audio.volume + delta;
            if (v >= 1) {
                v = 1;
                stopFadeTimer();
            }
            setVolume(v);
        },
        onFinish: stopFadeTimer,
        interval: 0.01,
    });
};

// Fade out volume
export const fadeOut = (duration = 0.1) => {
    stopFadeTimer();

    _stopFadeTimer = Timer({
        duration,
        onTick: (_, delta) => {
            let v = audio.volume - delta;
            if (v <= 0) {
                v = 0;
                stopFadeTimer();
            }
            setVolume(v);
        },
        onFinish: stop,
        interval: 0.01,
    });
};

// Set audio volume
export const setVolume = (volume) => {
    audio.volume = volume;
};

// Mute audio
export const mute = () => {
    setVolume(0);
};

// Play audio
export const play = () => {
    stopFadeTimer();
    setVolume(1);

    audio.play();

};

// Play audio from given time
export const playFrom = (time) => {
    setVolume(1);
    play();
    setCurrentTime(time);
};

// Pause audio
export const pause = () => {
    fadeOut();
};

export const stop = () => {
    stopFadeTimer();
    audio.pause();
};

// Load audio from given source
export const load = (src) => {
    stop();
    audio.src = src;

    // Required for Safari/iOS
    audio.load();
};

// Set current time t
export const setCurrentTime = (t) => {
    audio.currentTime = t;
};

// Get current time
export const getCurrentTime = () => {
    return audio.currentTime;
};

// Add a time update listener that sends current time to the callback
// Return a function to remove the event listener
export const onTimeUpdate = (onTimeUpdate) => {
    const callback = () => {
        onTimeUpdate(audio.currentTime);
    };
    audio.addEventListener("timeupdate", callback);

    // return remove event listener function
    return () => {
        audio.removeEventListener("timeupdate", callback);
    };
};

// Load audio, and call canPlay when audio is ready
export const loadUntilAvailable = (src, canPlay) => {
    // The canplaythrough event is fired when the user agent can play the media,
    // and estimates that enough data has been loaded to play the media up to its end
    // without having to stop for further buffering of content.
    const removeListener = listenOnce("canplaythrough", canPlay);

    load(src);

    // If the ready state is already > 3, data is already loaded;
    // Call canPlay right away
    // https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/readyState
    if (audio.readyState > 3) {
        removeListener();
        canPlay();
        return () => {};
    }

    return removeListener;
};

// Listen once to the given event
// After that remove listener
export const listenOnce = (event, callback) => {
    const remove = () => {
        audio.removeEventListener(event, _callback);
    };

    const _callback = () => {
        remove();
        callback();
    };
    audio.addEventListener(event, _callback);

    return remove;
};
