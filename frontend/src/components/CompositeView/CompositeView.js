import React, { useState, useEffect, useRef } from "react";
import * as audio from "../../util/audio";
import { MEDIA_ROOT } from "../../config";
import { getCurrentTime, getTimeSince } from "../../util/time";
import Preload from "../Preload/Preload";
import ListenStripped from '../Listen/ListenStripped';
import Circle from '../Circle/Circle';
import FeedbackForm from "../FeedbackForm/FeedbackForm";

const PRELOAD = "PRELOAD";
const RECOGNIZE = "RECOGNIZE";

// CompositeView is an experiment view, that preloads a song, shows an explanation and plays audio
// Optionally, it can show an animation during playback
// Optionally, it can show a form during or after playback
const CompositeView = ({ instructions, view, section, feedback_form, config, onResult }) => {
    // Main component state
    const [state, setState] = useState({ view: PRELOAD });

    const setView = (view, data = {}) => {
        setState({ view, ...data });
    };

    const [running, setRunning] = useState(config.auto_play);
    const [started, setStarted] = useState(running);

    const submitted = useRef(false);

    // Track time
    const startTime = useRef(getCurrentTime());

    // Time ref, stores the time without updating the view
    const time = useRef(0);

    const onCircleTimerTick = (t) => {
        time.current = t;
    };

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
                    instruction={instructions.preload}
                    duration={config.ready_time}
                    url={MEDIA_ROOT + section.url}
                    onNext={() => {
                        setView(RECOGNIZE);
                    }}
                />
            );
        case RECOGNIZE:

            const formActive =
                (started && !config.listen_first) ||
                (started && config.listen_first && !running);

            return (
                <div className="aha__composite">
                    <div className="circle">
                        <Circle
                            key={instructions.during_presentation + config.decision_time}
                            running={running}
                            duration={config.decision_time}
                            onTick={onCircleTimerTick}
                            color="white"
                            animateCircle={config.show_animation}
                            onFinish={() => {
                                if (config.auto_advance) {
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
                        />
                        <div className="circle-content">
                            <div className="stationary">
                                <span className="ti-headphone"></span>
                            </div>
                        </div>
                    </div>
                    <ListenStripped
                        instruction={instructions.during_presentation}
                        className=""
                    />
                    {feedback_form && (
                    <FeedbackForm
                        formActive={formActive}
                        form={feedback_form.form}
                        buttonLabel={feedback_form.submit_label}
                        skipLabel={feedback_form.skip_label}
                        onResult={() => {
                            createResult({
                                type: "form",
                                decision_time: getTimeSince(startTime.current),
                                given_result: feedback_form.form,
                            })
                        }}
                    />)}
                </div>
            );
        default:
            return <div>Unknown view: {state.view}</div>;
    }
};

export default CompositeView;
