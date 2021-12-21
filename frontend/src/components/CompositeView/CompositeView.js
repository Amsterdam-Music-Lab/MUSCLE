import React, { useState, useEffect, useRef } from "react";

import { getCurrentTime, getTimeSince } from "../../util/time";
import { createProfile, createResult } from "../../API.js";
import { MEDIA_ROOT } from "../../config";
import FeedbackForm from "../FeedbackForm/FeedbackForm";
import Playback from "../Playback/Playback";

// CompositeView is an experiment view, that preloads a song, shows an explanation and plays audio
// Optionally, it can show an animation during playback
// Optionally, it can show a form during or after playback
const CompositeView = ({ instructions, view, participant, players, session, feedback_form, config, onNext, loadState }) => {
    // Main component state
    const resultBuffer = useRef([]);

    const [running, setRunning] = useState(players.config.auto_play);
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
        
        if (feedback_form.is_profile) {
            submitProfile({
                result
            })
        }
        else {
                submitResult({
                view,
                decision_time,
                players,
                result,
            });
        }
    };

    // Get a section url from given (nested) action
const getSectionUrl = (action) => {
    if (!action) {
        return "";
    }

    if (action.section && action.section.url) {
        return action.section.url;
    }

    if (action.next_round) {
        return getSectionUrl(action.next_round);
    }

    return "";
};


    const formActive =
        (started && !config.listen_first) ||
        (started && config.listen_first && !running);

    return (
        <div className="aha__composite">
            {players && (
            <Playback
                instructions={instructions}
                config={config}
                players={players}
                onCircleTimerTick={onCircleTimerTick}
                audio={audio}
                submitResult={submitResult}
            />)}
            {feedback_form && (
            <FeedbackForm
                formActive={formActive}
                form={feedback_form.form}
                buttonLabel={feedback_form.submit_label}
                skipLabel={feedback_form.skip_label}
                isSkippable={feedback_form.is_skippable}
                onResult={makeResult}
            />)}
        </div>
    );
};

export default CompositeView;
