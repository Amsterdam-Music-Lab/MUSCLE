import React, { useRef, useEffect } from "react";

import Circle from "../Circle/Circle";
import ListenCircle from "../ListenCircle/ListenCircle";

const AutoPlay = ({instruction, playConfig, playSection, time, startedPlaying, finishedPlaying, responseTime, className=''}) => {
    // player state
    
    const running = useRef(playConfig.auto_play);

    // Handle view logic
    useEffect(() => {        
        playSection(0)
    }, [playConfig, startedPlaying]);

    // Render component
    return (
        <div>
            <div className="circle">
                <Circle
                    running={running}
                    duration={responseTime}
                    color="white"
                    animateCircle={playConfig.show_animation}
                    onFinish={() => {
                        // Stop audio
                        finishedPlaying();
                    }}
                />
                <div className="circle-content">
                    {playConfig.show_animation
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
