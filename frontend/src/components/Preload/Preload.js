import React, { useEffect, useRef, useState } from "react";

import ListenFeedback from "../Listen/ListenFeedback";
import CountDown from "../CountDown/CountDown";
import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import { MEDIA_ROOT } from "../../config";
import classNames from "classnames";

// Preload is an experiment screen that continues after a given time or after an audio file has been preloaded
const Preload = ({ instruction, pageTitle, duration, sections, playConfig, onNext }) => {
    const timeHasPassed = useRef(false);
    const audioIsAvailable = useRef(false);
    const [loaderDuration, setLoaderDuration] = useState(duration);
    const [overtime, setOvertime] = useState(false);
    
    const onTimePassed = () => {
        timeHasPassed.current = true;
        setLoaderDuration(0);
        setOvertime(true);
        if (audioIsAvailable.current) {
            onNext();
        }
    };

    // Audio preloader
    useEffect(() => {        
        if (playConfig.play_method === 'BUFFER') {

            // Use Web-audio and preload sections in buffers            
            sections.map((section, index) => {
                // Clear buffers if this is the first section
                if (index === 0) {
                    webAudio.clearBuffers();
                }
                                
                // Load sections in buffer                
                return webAudio.loadBuffer(section.id, MEDIA_ROOT + section.url, () => {                    
                    if (index === (sections.length - 1)) {
                        audioIsAvailable.current = true;
                        if (timeHasPassed.current) {
                            onNext();
                        }                        
                    }                                        
                });
            })
        } else {
            if (playConfig.play_method === 'EXTERNAL') {                    
                webAudio.closeWebAudio();            
            }
            // Load audio until available
            // Return remove listener   
            return audio.loadUntilAvailable(MEDIA_ROOT + sections[0].url, () => {
                audioIsAvailable.current = true;
                if (timeHasPassed.current) {
                    onNext();
                }
            });            
        }              
    }, [sections, onNext]);
    
    return (
        <ListenFeedback
            className={classNames({ pulse: overtime || duration === 0 })}
            pageTitle={pageTitle}
            duration={loaderDuration}
            instruction={instruction}
            onFinish={onTimePassed}
            circleContent={duration >= 1 && <CountDown duration={duration} />}
        />
    );
};

export default Preload;
