import React, { useState, useEffect, useRef } from "react";

import { getCurrentTime, getTimeSince } from "../../util/time";
import { createProfile, createResult } from "../../API.js";
import { MEDIA_ROOT } from "../../config";
import FeedbackForm from "../FeedbackForm/FeedbackForm";

// CompositeView is an experiment view, that preloads a song, shows an explanation and plays audio
// Optionally, it can show an animation during playback
// Optionally, it can show a form during or after playback
const CompositeView = ({ instructions, view, participant, players, session, feedback_form, config, onNext, loadState }) => {
    // Main component state
    const resultBuffer = useRef([]);

    const [running, setRunning] = useState(players.config.auto_play);
    const [started, setStarted] = useState(running);

    const submitted = useRef(false);

    // Session result
    const submitResult = async (result) => {
        // Add data to result buffer
        resultBuffer.current.push(result || {});

        // When time_pass_break is set true on the current state and result type
        // indicates that time has passed; skip any next rounds

        const timePassBreak =
            state &&
            state.time_pass_break &&
            result.type === "time_passed";

        // Check if there is another round data available
        // if so, store the result data and call onNext
        if (state && state.next_round && !timePassBreak) {
            onNext();
            return;
        }

        // Merge result data with data from resultBuffer
        // NB: result data with same properties will be overwritten by later results
        const mergedResults = Object.assign(
            {},
            ...resultBuffer.current,
            result
        );

        // Create result data
        const data = {
            session,
            participant,
            result: mergedResults,
        };

        // Optionally add section to result data
        if (mergedResults.section) {
            data.section = mergedResults.section;
        }

        // Send data to API
        const action = await createResult(data);

        // Fallback: Call onNext, try to reload round
        if (!action) {
            onNext();
            return;
        }

        // Clear resultBuffer
        resultBuffer.current = [];

        // Check for preload_section_url in (nested) action
        const preloadUrl = getSectionUrl(action);

        if (preloadUrl) {
            // 100ms for fadeout
            setTimeout(() => {
                audio.load(MEDIA_ROOT + preloadUrl);
            }, 20);
        }

        // Init new state from action
        loadState(action);
    };

    const submitProfile = async (result) => {
        // Send data to server
        const response = await createProfile({
            result,
            session: session.id,
            participant,
        });

        // Log error when createProfile failed
        if (!response || !response.status === "ok") {
            console.error("Could not store question");
        }

        // Continue
        onNext();
    };


    // Create result data in this wrapper function
    const makeResult = (result) => {
        const decision_time = result.type=='time_passed'? config.decision_time : getTimeSince(startTime.current);
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
