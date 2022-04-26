import React, { useState, useEffect, useRef } from "react";

import * as audio from "../../util/audio";
import { MEDIA_ROOT } from "../../config";

import AutoPlay from "./Autoplay";
import PlayButton from "../PlayButton/PlayButton";
import MultiPlayer from "./MultiPlayer";

const AUTOPLAY = "AUTOPLAY";
const BUTTON = "BUTTON";
const MULTIPLE = "MULTIPLE";

const Playback = ({playerType, sections, instruction, preloadMessage, autoAdvance, decisionTime, playConfig, time, submitResult, startedPlaying, finishedPlaying}) => {
    
    const audioIsAvailable = useRef(false);
    const timeHasPassed = useRef(false);

    const [url, setUrl] = useState(MEDIA_ROOT + sections[0].url)

    useEffect(() => {
        // Load audio until available
        // Return remove listener
        return audio.loadUntilAvailable(url, () => {
            audioIsAvailable.current = true;
            // if (timeHasPassed.current) {
            //     onNext();
            // }
        });
    }, [[url]]);

    const playSection = (index=0) => {
        if (sections[index].url !== url) {
            setUrl(MEDIA_ROOT + sections[index].url);
        }
        audio.pause();
        audio.setVolume(1);
        if (!playConfig.mute) {
            audio.playFrom(Math.max(0, playConfig.playhead));
            startedPlaying();
        } 
    };

    // if (autoAdvance) {
    //     // Create a time_passed result
    //     submitResult({
    //         type: "time_passed",
    //         decision_time: decisionTime,
    //         section: section.id
    //     });
    // }
    
    // render view
    const render = (view) => {
        const attrs = {
            sections,
            instruction,
            preloadMessage,
            autoAdvance,
            decisionTime,
            playConfig,
            time,
            submitResult,
            startedPlaying,
            finishedPlaying,
            playSection,
        };

        switch (view) {
            case AUTOPLAY:
                return <AutoPlay {...attrs} />;
            case BUTTON:
                return <PlayButton {...attrs} />;
            case MULTIPLE:
                return <MultiPlayer {...attrs} />;
            default:
                return <div>Unknown player view {view}</div>;
        }
    };

    return (
        <div className="aha__playback">
            <div className="playback">{render(playerType)}</div>
        </div>
    );
}
export default Playback;
