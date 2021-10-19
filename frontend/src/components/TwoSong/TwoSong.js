import React, { useState, useEffect, useRef } from "react";
import * as audio from "../../util/audio";
import { MEDIA_ROOT } from "../../config";
import Preload from "../Preload/Preload";
import TwoPlayer from "../TwoPlayer/TwoPlayer";
import { getCurrentTime, getTimeSince } from "../../util/time";

const PRELOAD = "PRELOAD";
const PLAYER = "PLAYER";

// TwoSong is an experiment view, that lets users play 2 sections
// and shows a single question with two customizable buttons
const TwoSong = ({
    button1_color,
    button1_label,
    button2_color,
    button2_label,
    config,
    instruction,
    introduction,
    onResult,
    ready_message,
    section1_color,
    section1_label,
    section1,
    section2_color,
    section2_label,
    section2,
    view,
    listen_first,
}) => {
    // Main component state
    const [state, setState] = useState({ view: PRELOAD });

    const setView = (view, data = {}) => {
        setState({ view, ...data });
    };

    // Track time
    const startTime = useRef(getCurrentTime());
    const submitted = useRef(false);

    // Create result data in this wrapper function
    const createResult = (result) => {
        // Prevent multiple submissions
        if (submitted.current) {
            return;
        }
        submitted.current = true;

        // Stop audio
        audio.pause();

        // setRunning(false);

        // Result callback
        onResult({
            view,
            section1,
            section2,
            config,
            result,
        });
    };

    // Handle view logic
    useEffect(() => {
        switch (state.view) {
            case PLAYER:
                // Play audio at start time
                startTime.current = getCurrentTime();
                break;
            default:
            // nothing
        }

        // Clean up
        return () => {
            audio.pause();
        };
    }, [state, config]);

    // Render component based on view
    switch (state.view) {
        case PRELOAD:
            return (
                <Preload
                    instruction={ready_message}
                    duration={config.ready_time}
                    url={MEDIA_ROOT + section1.url}
                    onNext={() => {
                        setView(PLAYER);
                    }}
                />
            );
        case PLAYER:
            return (
                <TwoPlayer
                    key={PLAYER}
                    introduction={introduction}
                    instruction={instruction}
                    button1Label={button1_label}
                    button1Color={button1_color}
                    button2Label={button2_label}
                    button2Color={button2_color}
                    section1={section1}
                    section1Color={section1_color}
                    section1Label={section1_label}
                    section2={section2}
                    section2Color={section2_color}
                    section2Label={section2_label}
                    listenFirst={listen_first}
                    onButton1Click={(stats = {}) => {
                        createResult({
                            ...stats,
                            type: "button1",
                            decision_time: getTimeSince(startTime.current),
                            given_result: 1,
                        });
                    }}
                    onButton2Click={(stats = {}) => {
                        createResult({
                            ...stats,
                            type: "button2",
                            decision_time: getTimeSince(startTime.current),
                            given_result: 2,
                        });
                    }}
                />
            );

        default:
            return <div>Unknown view: {state.view}</div>;
    }
};

export default TwoSong;
