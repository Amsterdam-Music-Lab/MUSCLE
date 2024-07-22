import React, { useRef } from "react";
import Circle from "../Circle/Circle";

interface ListenProps {
    circleContent?: React.ReactNode;
    instruction: string;
    duration?: number;
    onFinish: () => void;
    color?: string;
    running?: boolean;
    className?: string;
}

/** Listen is a base view for block views without user input */
const Listen = ({
    circleContent = null,
    instruction,
    duration = 0.01,
    onFinish,
    color = "white",
    running = true,
    className = "",
}: ListenProps) => {
    // Time ref, stores the time without updating the view
    const time = useRef(0);

    const onCircleTimerTick = (t: number) => {
        time.current = t;
    };

    return (
        <div
            className={
                "aha__listen d-flex flex-column justify-content-center align-items-center " +
                className
            }
        >
            {/* Circle */}
            <div className="circle">
                <Circle
                    key={instruction + duration}
                    running={running}
                    duration={duration}
                    onTick={onCircleTimerTick}
                    onFinish={onFinish}
                    color={color}
                />
                <div className="circle-content">{circleContent}</div>
            </div>

            {/* Instruction */}
            <div className="instruction d-flex justify-content-center align-items-center">
                <h3 className="text-center">{instruction}</h3>
            </div>
        </div>
    );
};

export default Listen;
