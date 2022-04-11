import React, { useState, useEffect, useRef } from "react";


import AutoPlay from "./Autoplay";
import PlayButton from "../PlayButton/PlayButton";
import MultiPlayer from "./MultiPlayer";

const AUTOPLAY = "AUTOPLAY";
const BUTTON = "BUTTON";
const MULTIPLE = "MULTIPLE";

const Playback = ({playerType, sections, instruction, preloadMessage, autoAdvance, playConfig, style, time, submitResult, startedPlaying, finishedPlaying}) => {

    // render view
    const render = (view) => {
        const attrs = {
            sections,
            instruction,
            preloadMessage,
            autoAdvance,
            playConfig,
            style,
            time,
            submitResult,
            startedPlaying,
            finishedPlaying
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
