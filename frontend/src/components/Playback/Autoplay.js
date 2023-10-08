import React, { useRef, useState, useEffect } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";

import Circle from "../Circle/Circle";
import ListenCircle from "../ListenCircle/ListenCircle";

const AutoPlay = ({instruction, preloadMessage, onPreloadReady, playConfig, sections, time, startedPlaying, finishedPlaying, responseTime, className=''}) => {
    // player state
    
    const running = useRef(playConfig.auto_play);
    
    const section = sections[0];

    const onCircleTimerTick = (t) => {
        time.current = t;
    };

    // Handle view logic
    useEffect(() => {        
        let latency = 0;
        // Play audio at start time            
        if (!playConfig.mute) {
            if (playConfig.play_method === 'BUFFER' && !playConfig.external_audio) {
                console.log('Autoplay buffer');
                latency = webAudio.getTotalLatency();
                webAudio.playBufferFrom(section.id, 0, Math.max(0, playConfig.playhead));
            } else {
                console.log('Autoplay HTML audio')
                audio.playFrom(Math.max(0, playConfig.playhead));
            }                    
            setTimeout(startedPlaying(), latency);
        }
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
                    onTick={onCircleTimerTick}
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
