import React, { useState, useEffect, useRef } from "react";
import classNames from "classnames";
import * as audio from "../../util/audio";
import ListenAdvanced from "../Listen/ListenAdvanced";
import Preload from "../Preload/Preload";
import PlayButton from "../PlayButton/PlayButton";
import ListenCircle from "../ListenCircle/ListenCircle";
import { MEDIA_ROOT } from "../../config";
import { getCurrentTime, getTimeSince } from "../../util/time";

const PRELOAD = "PRELOAD";
const RECOGNIZE = "RECOGNIZE";

// TwoAlternativeForced is an experiment view, that preloads a song, (auto)plays the audio
// and shows a single question with two customizable buttons
const TwoAlternativeForced = ({
    auto_advance,
    auto_play,
    button1_color,
    button1_label,
    button2_color,
    button2_label,
    config,
    instruction,
    introduction,
    listen_first,
    onResult,
    ready_message,
    section,
    view,
}) => {
    // Main component state
    const [state, setState] = useState({ view: PRELOAD });

    const setView = (view, data = {}) => {
        setState({ view, ...data });
    };

    const [running, setRunning] = useState(auto_play);
    const [started, setStarted] = useState(running);

    // Track time
    const startTime = useRef(getCurrentTime());

    // When playback is started (running), set started to true
    useEffect(() => {
        if (running && !started) {
            setStarted(true);
        }
    }, [running, started]);

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
                if (started || auto_play) {
                    audio.setCurrentTime(0);
                    audio.playFrom(0);
                    startTime.current = getCurrentTime();
                }
                break;
            default:
            // nothing
        }

        // Clean up
        return () => {
            audio.pause();
        };
    }, [state, config, auto_play, started]);

    // Render component based on view
    switch (state.view) {
        case PRELOAD:
            return (
                <Preload
                    instruction={ready_message}
                    duration={config.ready_time}
                    url={MEDIA_ROOT + section.url}
                    onNext={() => {
                        setView(RECOGNIZE);
                    }}
                />
            );
        case RECOGNIZE:
            const circleContent = started ? (
                <ListenCircle
                    duration={config.decision_time}
                    histogramRunning={running}
                    countDownRunning={running}
                />
            ) : (
                <PlayButton
                    className="anim anim-fade-in"
                    onClick={() => {
                        setRunning(true);
                    }}
                />
            );

            const buttonsActive =
                (started && !listen_first) ||
                (started && listen_first && !running);

            return (
                <ListenAdvanced
                    className={classNames("wide-buttons", { pulse: !started })}
                    running={running}
                    key={RECOGNIZE}
                    autoPlay={auto_play}
                    duration={config.decision_time}
                    introduction={introduction}
                    instruction={instruction}
                    button1Label={button1_label}
                    button1Color={button1_color}
                    button2Label={button2_label}
                    button2Color={button2_color}
                    buttonsActive={buttonsActive}
                    circleContent={circleContent}
                    onFinish={() => {
                        if (auto_advance) {
                            // Create a time_passed result
                            createResult({
                                type: "time_passed",
                                decision_time: config.decision_time,
                            });
                        } else {
                            // Stop audio
                            audio.pause();
                            setRunning(false);
                        }
                    }}
                    onButton1Click={() => {
                        createResult({
                            type: "button1",
                            decision_time: getTimeSince(startTime.current),
                            given_result: button1_label,
                        });
                    }}
                    onButton2Click={() => {
                        createResult({
                            type: "button2",
                            decision_time: getTimeSince(startTime.current),
                            given_result: button2_label,
                        });
                    }}
                />
            );
        default:
            return <div>Unknown view: {state.view}</div>;
    }
};

export default TwoAlternativeForced;
