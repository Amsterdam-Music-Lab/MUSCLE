import { useEffect, useState } from "react";
import classNames from "classnames";

import Circle from "../Circle/Circle";
import * as audio from "../../util/audio";
import * as webAudio from "../../util/webAudio";
import Section from "@/types/Section";

interface PreloadProps {
    sections: Section[];
    playMethod: string;
    duration: number;
    preloadMessage: string;
    pageTitle: string;
    onNext: () => void;
}

/** Preload is an experiment screen that continues after a given time or after an audio file has been preloaded */
const Preload = ({ sections, playMethod, duration, preloadMessage, onNext }: PreloadProps) => {
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

                await Promise.all(sections.map((section) => fetch(section.url)));

                return onNext();
            }

            if (playMethod === 'BUFFER') {

                // Use Web-audio and preload sections in buffers

                sections.forEach((section, index) => {

                    // skip Preload if the section has already been loaded in the previous action
                    if (webAudio.checkSectionLoaded(section) && sections.length === 1) {
                        setAudioAvailable(true);
                        return;
                    }

                    // Clear buffers if this is the first section
                    if (index === 0) {
                        webAudio.clearBuffers();
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
                sections.forEach((section, index) => {
                    return audio.loadUntilAvailable(section.url, () => {
                        if (index === (sections.length - 1)) {
                            setAudioAvailable(true);
                        }
                    });
                })
            }
        }

        preloadResources();
    }, [sections, playMethod, onNext]);

    return (
        <div className={
            "aha__preload d-flex flex-column justify-content-center align-items-center " +
            classNames({ pulse: overtime || duration === 0 })
        }>
        <Circle
            key={preloadMessage + duration}
            duration={loaderDuration}
            onFinish={onTimePassed}
        />
        {preloadMessage && (
            <div className="instruction d-flex justify-content-center align-items-center">
                <h3 className="text-center">{preloadMessage}</h3>
            </div>
        )}
        </div>
    );
};

export default Preload;
