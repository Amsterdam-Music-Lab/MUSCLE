import React, { useRef, useState, useEffect } from "react";

import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { MEDIA_ROOT } from "../../config";

import Circle from "../Circle/Circle";
import ListenCircle from "../ListenCircle/ListenCircle";
import Preload from "../Preload/Preload";

const PRELOAD = "PRELOAD";
const RECOGNIZE = "RECOGNIZE";


const AutoPlay = ({instruction, preloadMessage, onPreloadReady, playConfig, sections, time, startedPlaying, finishedPlaying, responseTime, className=''}) => {
    // player state
    const [state, setState] = useState({ view: PRELOAD });
    const running = useRef(playConfig.auto_play);
    const setView = (view, data = {}) => {
        setState({ view, ...data });
    }

    const section = sections[0];

    const onCircleTimerTick = (t) => {
        time.current = t;
    };


    // Handle view logic
    useEffect(() => {
        switch (state.view) {
            case RECOGNIZE:              
                // Only initialize webaudio if section is local
                let latency = webAudio.initWebAudio(section['url']);             
                // Play audio at start time            
                if (!playConfig.mute) {
                    audio.playFrom(Math.max(0, playConfig.playhead));
                }
                // Compensate for audio latency and set state to playing
                setTimeout(startedPlaying(), latency);                
                break;
            default:
            // nothing
        }

        // Clean up
        return () => {
            audio.pause();
        };
    }, [state, playConfig, startedPlaying]);


    // Render component based on view
    switch (state.view) {
        case PRELOAD:           
            return (
                <Preload
                    instruction={preloadMessage}
                    duration={playConfig.ready_time}
                    url={MEDIA_ROOT + section.url}
                    onNext={() => {                        
                        setView(RECOGNIZE);
                        onPreloadReady();
                    }}
                />
            );
        case RECOGNIZE:            
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
                                    <span className="ti-headphone"></span>
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
            default:
                return <div>Unknown view: {state.view}</div>;
        }
}
export default AutoPlay;
