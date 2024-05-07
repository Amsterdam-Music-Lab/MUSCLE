import React, { useEffect, useState } from "react";
import classNames from "classnames";

import { MEDIA_ROOT } from "@/config";
import ListenFeedback from "../Listen/ListenFeedback";
import CountDown from "../CountDown/CountDown";
import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";

// Preload is an experiment screen that continues after a given time or after an audio file has been preloaded
const Preload = ({ sections, playMethod, duration, preloadMessage, pageTitle, onNext }) => {
    const [audioAvailable, setAudioAvailable] = useState(false);
    const [overtime, setOvertime] = useState(false);
    const [loaderDuration, setLoaderDuration] = useState(duration);
    
    const onTimePassed = () => {
        setLoaderDuration(0);
        setOvertime(true);
        if (audioAvailable) {
            onNext();
        }
    };

    // Audio preloader
    useEffect(() => {
        const preloadResources = async () => {
            if (playMethod === 'NOAUDIO') {

                await Promise.all(sections.map((section) => fetch(MEDIA_ROOT + section.url)));

                return onNext();
            }

            if (playMethod === 'BUFFER') {
                // Use Web-audio and preload sections in buffers            
                sections.forEach((section, index) => {
                    // skip Preload if the section has already been loaded in the previous action
                    if (webAudio.checkSectionLoaded(section)) {
                        if (index === (sections.length - 1)) {                            
                            setAudioAvailable(true);                       
                        }
                        return;
                    }

                    // Load sections in buffer                
                    return webAudio.loadBuffer(section.id, section.url, () => {                    
                        if (index === (sections.length - 1)) {                            
                            setAudioAvailable(true);                  
                        }                                        
                    });
                })
            } else {
                if (playMethod === 'EXTERNAL') {                    
                    webAudio.closeWebAudio();        
                }
                // Load audio until available
                // Return remove listener   
                return audio.loadUntilAvailable(section.url, () => {
                    if (index === (sections.length - 1)) {                            
                        setAudioAvailable(true);                  
                    }
                });            
            }
        }

        preloadResources();
        // on destroy, clean up buffers
        return webAudio.clearBuffers();    
    }, [sections, playMethod, onNext]);
    
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
