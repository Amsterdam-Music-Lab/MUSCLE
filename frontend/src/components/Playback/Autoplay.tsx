import { useEffect, useState } from "react";

import Circle from "../Circle/Circle";
import AnimatedCircleContent from "../AnimatedCircleContent/AnimatedCircleContent";

interface AutoPlayProps {
    instruction?: string;
    showAnimation: boolean;
    playSection: (section: number) => void;
    startedPlaying: boolean;
    finishedPlaying: () => void;
    responseTime: number;
    className?: string;
}

const AutoPlay = ({ instruction, showAnimation, playSection, startedPlaying, finishedPlaying, responseTime, className = '' }: AutoPlayProps) => {

    const [running, setRunning] = useState(true);

    // Handle view logic
    useEffect(() => {
        playSection(0)
    }, [playSection, startedPlaying]);

    return (
        <div>
            <div className="circle">
                <Circle
                    running={running}
                    duration={responseTime}
                    color="white"
                    animateCircle={showAnimation}
                    onFinish={() => {
                        // Stop audio
                        setRunning(false);
                        finishedPlaying();
                    }}
                />
                <div className="circle-content">
                    {showAnimation
                        ? <AnimatedCircleContent
                            duration={responseTime}
                            histogramRunning={running}
                            countDownRunning={running}
                        />
                        : <div className="stationary">
                            <span className="fa-solid fa-headphones fa-6x"></span>
                        </div>
                    }
                </div>
            </div>
            <div className={"aha__listen d-flex flex-column justify-content-center align-items-center " + className}
            >
                {/* Instruction */}
                {instruction && (<div className="instruction d-flex justify-content-center align-items-center">
                    <h3 className="text-center">{instruction}</h3>
                </div>)}
            </div>
        </div>
    )
}
export default AutoPlay;
