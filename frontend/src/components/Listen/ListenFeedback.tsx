import React, { useRef } from "react";
import Circle from "../Circle/Circle";
import { Button } from "@/components/ui";

interface ListenFeedbackProps {
    circleContent?: React.ReactNode;
    instruction: string;
    duration?: number;
    onFinish: () => void;
    color?: string;
    running?: boolean;
    className?: string;
    onNoClick?: () => void;
    onYesClick?: () => void;
    buttons?: {
        no: string;
        yes: string;
    };
}

/** ListenFeedback is a base view for block views with a yes and no button */
const ListenFeedback = ({
    circleContent = null,
    instruction,
    duration = 0.01,
    onFinish,
    color = "white",
    running = true,
    className = "",
    onNoClick,
    onYesClick,
    buttons
}: ListenFeedbackProps) => {
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
            {instruction && (
                <div className="instruction d-flex justify-content-center align-items-center">
                    <h3 className="text-center">{instruction}</h3>
                </div>
            )}

            {/* Buttons */}
            {buttons && (
                <div className="buttons d-flex justify-content-around p-3 w-100">
                    {/* No-button */}
                    {onNoClick && (
                        <Button
                            key={"no"}
                            className="btn-negative"
                            onClick={onNoClick}
                            title={buttons.no}
                        />
                    )}

                    {/* Yes-button */}
                    {onYesClick && (
                        <Button
                            key={"yes"}
                            className="btn-positive"
                            onClick={onYesClick}
                            title={buttons.yes}
                        />
                    )}
                </div>
            )}
        </div>
    );
};

export default ListenFeedback;
