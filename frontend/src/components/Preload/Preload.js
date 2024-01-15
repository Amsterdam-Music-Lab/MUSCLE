import React, { useEffect, useState } from "react";
import classNames from "classnames";


import ListenFeedback from "../Listen/ListenFeedback";
import CountDown from "../CountDown/CountDown";
import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";

// Preload is an experiment screen that continues after a given time or after an audio file has been preloaded
const Preload = ({ sections, playMethod, duration, preloadMessage, pageTitle, onNext }) => {
    const [timePassed, setTimePassed] = useState(false);
    const [audioAvailable, setAudioAvailable] = useState(false);
    const [overtime, setOvertime] = useState(false);
    const [loaderDuration, setLoaderDuration] = useState(duration);
    
    const onTimePassed = () => {
        setTimePassed(true)
        setLoaderDuration(0);
        setOvertime(true);
        if (audioAvailable) {
            onNext();
        }
    };

    // Audio preloader
    useEffect(() => {        
        if (playMethod === 'BUFFER') {

            // Use Web-audio and preload sections in buffers            
            sections.map((section, index) => {
                // skip Preload if the section has already been loaded in the previous action
                if (webAudio.checkSectionLoaded(section)) {
                    onNext();
                    return undefined;
                }
                // Clear buffers if this is the first section
                if (index === 0) {
                    webAudio.clearBuffers();
                }
                                
                // Load sections in buffer                
                return webAudio.loadBuffer(section.id, section.url, () => {                    
                    if (index === (sections.length - 1)) {
                        setAudioAvailable(true);
                        if (timePassed) {
                            onNext();
                        }                        
                    }                                        
                });
            })
        } else {
            if (playMethod === 'EXTERNAL') {                    
                webAudio.closeWebAudio();        
            }
            // Load audio until available
            // Return remove listener   
            return audio.loadUntilAvailable(sections[0].url, () => {
                setAudioAvailable(true);
                if (timePassed) {
                    onNext();
                }
            });            
        }              
    }, [sections, playMethod, onNext, timePassed]);
    
    return (
        <ListenFeedback
            className={classNames({ pulse: overtime || duration === 0 })}
            pageTitle={pageTitle}
            duration={loaderDuration}
            instruction={preloadMessage}
            onFinish={onTimePassed}
            circleContent={duration >= 1 && <CountDown duration={duration} />}
        />
    );
};

export default Preload;
