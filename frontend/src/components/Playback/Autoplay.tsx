import { useEffect, useState } from "react";

import Circle from "../Circle/Circle";
import CountDown from "../CountDown/CountDown";
import Histogram from "../Histogram/Histogram";

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
        <div className={"aha__autoplay d-flex flex-column justify-content-center align-items-center " + className}>
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
                        ?
                        <div>
                            <CountDown duration={responseTime} running={running} />
                            <div className="aha__histogram-container">
                                <Histogram running={running} />
                            </div>
                        </div>
                        : <div className="stationary">
                            <span className="fa-solid fa-headphones fa-6x"></span>
                        </div>
                    }
                </div>
            </div>
            {/* Instruction */}
            {instruction && (<div className="instruction d-flex justify-content-center align-items-center">
                <h3 className="text-center">{instruction}</h3>
            </div>)}
        </div>
    )
}
export default AutoPlay;
