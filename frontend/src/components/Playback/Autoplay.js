import React, { useRef, useEffect } from "react";

import Circle from "../Circle/Circle";
import ListenCircle from "../ListenCircle/ListenCircle";

const AutoPlay = ({playbackArgs, playSection, time, finishedPlaying, responseTime, className=''}) => {
    // player state
    
    const running = useRef(true);

    const onCircleTimerTick = (t) => {
        time.current = t;
    };

    // Handle view logic
    useEffect(() => {
        playSection(0);
    });

    // Render component
    return (
        <div>
            <div className="circle">
                <Circle
                    running={running}
                    duration={responseTime}
                    color="white"
                    animateCircle={playbackArgs.show_animation}
                    onTick={onCircleTimerTick}
                    onFinish={() => {
                        // Stop audio
                        finishedPlaying();
                    }}
                />
                <div className="circle-content">
                    {playbackArgs.show_animation
                        ? <ListenCircle
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
            <div className={
                "aha__listen d-flex flex-column justify-content-center align-items-center " +
                className
            }
            >
            {/* Instruction */}
            {playbackArgs.instruction && (<div className="instruction d-flex justify-content-center align-items-center">
                <h3 className="text-center">{playbackArgs.instruction}</h3>
            </div>)}
        </div>
    </div>
    )   
}
export default AutoPlay;
