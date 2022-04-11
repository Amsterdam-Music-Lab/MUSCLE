import React, { useState, useRef, useEffect } from "react";
import * as audio from "../../util/audio";

import PlayerSmall from "../PlayButton/PlayerSmall";

import { MEDIA_ROOT } from "../../config";


const MultiPlayer = ({sections, instruction, playConfig, style}) => {
    const cancelEvents = useRef(null);
    const [playing, setPlaying] = useState(0);

    const cancelActiveEvents = () => {
        // cancel events
        if (cancelEvents.current) {
            cancelEvents.current();
            cancelEvents.current = null;
        }
    };

    const playMedia = (url) => {
        audio.pause();

        cancelActiveEvents();
        cancelEvents.current = audio.listenOnce("ended", setPlaying);

        audio.loadUntilAvailable(MEDIA_ROOT+url, () => {
            audio.setVolume(1);
            audio.playFrom(0);
        });
    };

    return (
        <div className="aha__multiplayer d-flex justify-content-between">
        {Object.keys(sections).map((index) => (
            <PlayerSmall
                style={style}
                onClick={() => {
                    playMedia(sections[index].url);
                }}
            />
        ))}
        </div>
    )
}
export default MultiPlayer;
