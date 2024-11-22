/**
 * OnTick callback type
 * @param time - current time in seconds
 * @param delta - time since last tick in seconds
 */
type TOnTick = (time: number, delta: number) => void;

interface TimerParams {
    time?: number;          // initial time in seconds
    duration: number;       // duration in seconds
    onTick?: TOnTick;
    onFinish?: () => void;
    interval?: number;
}

// Timer component with callback
export const Timer = ({
    time = 0,
    duration,
    onTick,
    onFinish,
    interval = 0.1,
}: TimerParams) => {
    let lastTimestamp = performance.now();
    let lastTime = time;
    let running = true;

    const callback = (timestamp: number) => {
        if (!running) {
            return;
        }

        const delta = (timestamp - lastTimestamp) / 1000;
        time = Math.min(duration, time + delta);

        // timer finished
        if (time === duration) {
            return onFinish ? onFinish() : void 0;
        }

        // callback after interval
        if (time - lastTime > interval) {
            lastTime = time;

            // tick
            onTick && onTick(time, delta);
        }

        lastTimestamp = timestamp;

        window.requestAnimationFrame(callback);
    };
    window.requestAnimationFrame(callback);

    // return stop function
    return () => {
        running = false;
    };
};

export default Timer;
