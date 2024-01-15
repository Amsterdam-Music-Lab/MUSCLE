import React, { useEffect } from "react";

import Circle from "../Circle/Circle";
import ListenCircle from "../ListenCircle/ListenCircle";

const AutoPlay = ({instruction, showAnimation, playSection, startedPlaying, finishedPlaying, responseTime, className=''}) => {

    // Handle view logic
    useEffect(() => {        
        playSection(0)
    }, [playSection, startedPlaying]);

    // Render component
    return (
        <div>
            <div className="circle">
                <Circle
                    running={true}
                    duration={responseTime}
                    color="white"
                    animateCircle={showAnimation}
                    onFinish={() => {
                        // Stop audio
                        finishedPlaying();
                    }}
                />
                <div className="circle-content">
                    {showAnimation
                        ? <ListenCircle
                            duration={responseTime}
                            histogramRunning={true}
                            countDownRunning={true}
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
