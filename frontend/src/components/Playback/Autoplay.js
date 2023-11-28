import React, { useRef, useEffect } from "react";

import { playAudio } from "../../util/audioControl";

import Circle from "../Circle/Circle";
import ListenCircle from "../ListenCircle/ListenCircle";

const AutoPlay = ({sections, mute, playhead, playMethod, instruction, showAnimation, time, startedPlaying, finishedPlaying, responseTime, className=''}) => {
    // player state
    
    const running = useRef(true);

    const onCircleTimerTick = (t) => {
        time.current = t;
    };

    // Handle view logic
    useEffect(() => {        
        let latency = 0;
        // Play audio at start time            
        if (mute) {            
            latency = playAudio(sections[0], playMethod, playhead);          
            // Compensate for audio latency and set state to playing
            setTimeout(startedPlaying(), latency);
        }
    }, [sections, mute, playMethod, playhead, startedPlaying]);

    // Render component
    return (
        <div>
            <div className="circle">
                <Circle
                    running={running}
                    duration={responseTime}
                    color="white"
                    animateCircle={showAnimation}
                    onTick={onCircleTimerTick}
                    onFinish={() => {
                        // Stop audio
                        finishedPlaying();
                    }}
                />
                <div className="circle-content">
                    {showAnimation
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
            {instruction && (<div className="instruction d-flex justify-content-center align-items-center">
                <h3 className="text-center">{instruction}</h3>
            </div>)}
        </div>
    </div>
    )   
}
export default AutoPlay;
