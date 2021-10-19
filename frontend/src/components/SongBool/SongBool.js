import React, { useState, useEffect, useRef } from "react";
import * as audio from "../../util/audio";
import ListenFeedback from "../Listen/ListenFeedback";
import Preload from "../Preload/Preload";
import ListenCircle from "../ListenCircle/ListenCircle";
import { MEDIA_ROOT } from "../../config";
import { getCurrentTime, getTimeSince } from "../../util/time";

const PRELOAD = "PRELOAD";
const RECOGNIZE = "RECOGNIZE";

// SongBool is an experiment view, that preloads a song, plays the audio
// and shows a single question with yes/no buttons
const SongBool = ({ instruction, view, buttons, section, config, onResult }) => {
    // Main component state
    const [state, setState] = useState({ view: PRELOAD });

    const setView = (view, data = {}) => {
        setState({ view, ...data });
    };

    const [running, setRunning] = useState(true);

    const submitted = useRef(false);

    // Track time
    const startTime = useRef(getCurrentTime());

    // Create result data in this wrapper function
    const createResult = (result) => {
        // Prevent multiple submissions
        if (submitted.current) {
            return;
        }
        submitted.current = true;

        // Stop audio
        audio.pause();

        setRunning(false);

        // Result callback
        onResult({
            view,
            section,
            config,
            result,
        });
    };

    // Handle view logic
    useEffect(() => {
        switch (state.view) {
            case RECOGNIZE:
                // Play audio at start time
                audio.playFrom(0);
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
                    instruction={instruction}
                    duration={config.ready_time}
                    url={MEDIA_ROOT + section.url}
                    onNext={() => {
                        setView(RECOGNIZE);
                    }}
                />
            );
        case RECOGNIZE:
            return (
                <ListenFeedback
                    running={running}
                    key={RECOGNIZE}
                    duration={config.decision_time}
                    instruction={instruction}
                    buttons={buttons}
                    circleContent={
                        <ListenCircle
                            duration={config.decision_time}
                            histogramRunning={running}
                            countDownRunning={running}
                        />
                    }
                    onFinish={() => {
                        createResult({
                            type: "time_passed",
                            decision_time: config.decision_time,
                        });
                    }}
                    onNoClick={() => {
                        createResult({
                            type: "no",
                            decision_time: getTimeSince(startTime.current),
                            given_result: false,
                        });
                    }}
                    onYesClick={() => {
                        createResult({
                            type: "yes",
                            decision_time: getTimeSince(startTime.current),
                            given_result: true,
                        });
                    }}
                />
            );
        default:
            return <div>Unknown view: {state.view}</div>;
    }
};

export default SongBool;
