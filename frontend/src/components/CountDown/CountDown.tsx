import React, { useState, useEffect } from "react";
import Timer from "@/util/timer";
import classNames from "classnames";

interface CountDownProps {
    duration: number;
    running?: boolean;
}

// CountDown to zero
const CountDown = ({ duration, running = true }: CountDownProps) => {
    // automatic timer
    const [time, setTime] = useState(0);
    const [zero, setZero] = useState(false);

    useEffect(() => {
        if (!running) {
            return;
        }

        // start time when running
        return Timer({
            duration,
            onTick: (t) => setTime(Math.min(t, duration)),
            onFinish: () => setZero(true),
        });
    }, [duration, running]);

    return (
        <h1
            className={classNames("aha__count-down", { active: running, zero })}
        >
            {zero ? "0" : Math.ceil(duration - time)}
        </h1>
    );
};

export default CountDown;
