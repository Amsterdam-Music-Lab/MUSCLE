import { useEffect, useState } from "react";
import Timer from "@/util/timer";

interface CircleProps {
    startTime?: number;
    duration?: number;
    color?: string;
    onTick?: (time: number) => void;
    onFinish?: () => void;
    radius?: number;
    strokeWidth?: number;
    running?: boolean;
    animateCircle?: boolean;
}

// Circle shows a counterclockwise circular animation
const Circle = ({
    startTime = 0,
    duration = 0,
    color = "white",
    onTick,
    onFinish,
    radius = 85,
    strokeWidth = 7,
    running = true,
    animateCircle = true,
}: CircleProps) => {

    // automatic timer
    const [time, setTime] = useState(startTime);

    // Time animation
    useEffect(() => {
        if (!running) {
            return;
        }

        // Create timer and return stop function
        return Timer({
            time: startTime,
            duration,
            onTick: (t) => {
                setTime(Math.min(t, duration));
                onTick?.(t);
            },
            onFinish: () => {
                onFinish?.();
            },
        });
    }, [running, duration, onTick, onFinish, startTime]);

    const diameter = radius * 2;
    const circumference = diameter * Math.PI;
    const size = diameter + strokeWidth;
    let style = {};
    if (animateCircle) {
        const perc = duration
            ? Math.min(1, (time + (running || time > 0 ? 0.1 : 0)) / duration)
            : 0;
        style = {
            strokeDasharray: circumference + " " + circumference,
            strokeDashoffset: perc * circumference,
        }
    }
    // while running, add 0.1 to compensate for the css transition delay
    return (
        <div
            className="aha__circle"
            style={{
                width: size,
                height: size,
            }}
        >
            <svg
                width={size}
                height={size}
                viewBox={"0 0 " + size + " " + size}
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <circle
                    opacity="0.25"
                    cx={radius + strokeWidth / 2}
                    cy={radius + strokeWidth / 2}
                    r={radius}
                    stroke="white"
                    strokeWidth={strokeWidth}
                />
                <circle
                    className="circle-percentage"
                    cx={radius + strokeWidth / 2}
                    cy={radius + strokeWidth / 2}
                    r={radius}
                    stroke={color}
                    strokeWidth={strokeWidth}
                    style={style}
                />
            </svg>
        </div>
    );
};

export default Circle;
