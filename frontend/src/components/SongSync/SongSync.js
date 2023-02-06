import React, { useState, useEffect, useRef } from "react";
import * as audio from "../../util/audio";
import ListenFeedback from "../Listen/ListenFeedback";
import ListenCircle from "../ListenCircle/ListenCircle";
import Preload from "../Preload/Preload";
import { MEDIA_ROOT } from "../../config";
import { getCurrentTime, getTimeSince } from "../../util/time";

const PRELOAD = "PRELOAD";
const RECOGNIZE = "RECOGNIZE";
const SILENCE = "SILENCE";
const SYNC = "SYNC";

// SongSync is an experiment view, with four stages:
// - PRELOAD: Preload a song
// - RECOGNIZE: Play audio, ask if participant recognizes the song
// - SILENCE: Silence audio
// - SYNC: Continue audio, ask is position is in sync
const SongSync = ({
    view,
    section,
    instructions,
    buttons,
    config,
    result_id,
    onResult
}) => {
    // Main component state
    const [state, setState] = useState({ view: PRELOAD });
    const [running, setRunning] = useState(true);

    const setView = (view, data = {}) => {
        setState({ view, ...data });
    };

    const submitted = useRef(false);

    // Track time
    const startTime = useRef(getCurrentTime());

    // Create result data in this wrapper function
    const addResult = (result) => {
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
            config,
            result,
            
            // Keep result_id in custom data root
            result_id: result_id,
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
            case SYNC:
                // Play audio from sync start time
                const syncStart = Math.max(
                    0,
                    state.result.recognition_time +
                        config.silence_time +
                        config.continuation_offset
                );
                audio.playFrom(syncStart);
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
                    instruction={instructions.ready}
                    duration={config.ready_time}
                    url={MEDIA_ROOT + section}
                    onNext={() => {
                        setView(RECOGNIZE);
                    }}
                />
            );
        case RECOGNIZE:
            return (
                <ListenFeedback
                    running={running}
                    duration={config.recognition_time}
                    buttons={buttons}
                    circleContent={
                        <ListenCircle
                            duration={config.recognition_time}
                            histogramRunning={running}
                            countDownRunning={running}
                        />
                    }
                    instruction={instructions.recognize}
                    onFinish={() => {
                        addResult({
                            type: "time_passed",
                            recognition_time: config.recognition_time,
                        });
                    }}
                    onNoClick={() => {
                        addResult({
                            type: "not_recognized",
                            recognition_time: getTimeSince(startTime.current),
                        });
                    }}
                    onYesClick={() => {
                        setView(SILENCE, {
                            result: {
                                type: "recognized",
                                recognition_time: getTimeSince(
                                    startTime.current
                                ),
                            },
                        });
                    }}
                />
            );

        case SILENCE:
            return (
                <ListenFeedback
                    duration={config.silence_time}
                    circleContent={
                        <ListenCircle
                            duration={config.recognition_time}
                            histogramRunning={false}
                            countDownRunning={false}
                        />
                    }
                    instruction={instructions.imagine}
                    onFinish={() => {
                        setView(SYNC, { result: state.result });
                    }}
                />
            );

        case SYNC:
            return (
                <ListenFeedback
                    running={running}
                    duration={config.sync_time}
                    buttons={buttons}
                    circleContent={
                        <ListenCircle
                            duration={config.recognition_time}
                            countDownRunning={false}
                        />
                    }
                    instruction={instructions.correct}
                    onFinish={() => {
                        addResult(
                            Object.assign({}, state.result, {
                                sync_time: config.sync_time,
                                // Always the wrong answer!
                                continuation_correctness:
                                    !config.continuation_correctness,
                            })
                        );
                    }}
                    onNoClick={() => {
                        addResult(
                            Object.assign({}, state.result, {
                                sync_time: getTimeSince(startTime.current),
                                continuation_correctness: false,
                            })
                        );
                    }}
                    onYesClick={() => {
                        addResult(
                            Object.assign({}, state.result, {
                                sync_time: getTimeSince(startTime.current),
                                continuation_correctness: true,
                            })
                        );
                    }}
                />
            );
        default:
            return <div>Unknown view: {state.view}</div>;
    }
};

export default SongSync;
