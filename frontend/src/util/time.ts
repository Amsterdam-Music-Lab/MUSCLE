export const getCurrentTime = () => Date.now() / 1000;

export const getTimeSince = (time: number) => getCurrentTime() - time;

export const getAudioLatency = () => {
    if (window.sessionStorage.getItem('audioLatency') !== null) {
        return Number(window.sessionStorage.getItem('audioLatency'));
    } else {
        return NaN;
    }
}
