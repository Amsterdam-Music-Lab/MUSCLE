import React, { useState, useRef } from "react";
import * as audio from "../../util/audio";
import { getCurrentTime, getTimeSince } from "../../util/time";
import FeedbackForm from "../FeedbackForm/FeedbackForm";
import Playback from "../Playback/Playback";


// CompositeView is an experiment view, that preloads a song, shows an explanation and plays audio
// Optionally, it can show an animation during playback
// Optionally, it can show a form during or after playback
const CompositeView = ({ instructions, view, section, feedback_form, config, onResult }) => {
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

    const formActive =
        (started && !config.listen_first) ||
        (started && config.listen_first && !running)
    
    return (
        <div className="aha__composite">
            {section &&
            <Playback
                instructions={instructions}
                config={config}
                section={section}
                onCircleTimerTick={onCircleTimerTick}
                audio={audio}
                createResult={createResult}
            />
            }
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
};

export default CompositeView;
