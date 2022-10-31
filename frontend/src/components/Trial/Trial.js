import React, { useState, useRef, useCallback } from "react";
import classNames from "classnames";

import { getCurrentTime, getTimeSince } from "../../util/time";
import { createProfile, createResult } from "../../API.js";
import FeedbackForm from "../FeedbackForm/FeedbackForm";
import Playback from "../Playback/Playback";
import Button from "../Button/Button";

// Trial is an experiment view, that preloads a song, shows an explanation and plays audio
// Optionally, it can show an animation during playback
// Optionally, it can show a form during or after playback
const Trial = ({
    participant,
    session,
    playback,
    feedback_form,
    config,
    onNext,
    loadState,
}) => {
    // Main component state
    const resultBuffer = useRef([]);

    const [formActive, setFormActive] = useState(!config.listen_first);
    const [preloadReady, setPreloadReady] = useState(
        !playback?.play_config?.ready_time
    );

    const submitted = useRef(false);

    // This is used to keep track of the time a participant spends in this Trial view
    const startTime = useRef(getCurrentTime());

    // Time ref, stores the time without updating the view
    const time = useRef(0);
    const startTimer = useCallback(() => {
        startTime.current = getCurrentTime();
    }, []);

    // Session result
    const submitResult = useCallback(
        async (result) => {
            // Add data to result buffer
            resultBuffer.current.push(result || {});

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

            // Init new state from action
            loadState(action);
        },
        [loadState, onNext, participant, session]
    );

    const submitProfile = useCallback(
        async (result) => {
            // Send data to server
            const response = await createProfile({
                result,
                session: (session ? session.id : 0),
                participant,
            });

            // Log error when createProfile failed
            if (!response || !response.status === "ok") {
                console.error("Could not store question");
            }

            // Continue
            onNext();
        },
        [onNext, participant, session]
    );

    // Create result data in this wrapper function
    const makeResult = useCallback(
        (result) => {            
            // Prevent multiple submissions
            if (submitted.current) {
                return;
            }
            submitted.current = true;

            const decision_time = getTimeSince(startTime.current);
            const form = feedback_form ? feedback_form.form : [{}];

            if (result.type === "time_passed") {
                form.map((formElement) => (formElement.value = "TIMEOUT"));
            }

            if (feedback_form) {
                if (feedback_form.is_profile) {
                    submitProfile({
                        form,
                    });
                } else {
                    submitResult({
                        decision_time,
                        form,
                    });
                }
            } else {
                onNext();
            }
        },
        [feedback_form, onNext, submitProfile, submitResult]
    );

    const finishedPlaying = useCallback(() => {

        if (config.auto_advance) {

            // Create a time_passed result
            if (config.auto_advance_timer != null) {
                if (playback.player_type == 'BUTTON') {
                    startTime.current = getCurrentTime();
                }
                const id = setTimeout( () => {makeResult({type: "time_passed",});} , config.auto_advance_timer);

            } else {

                makeResult({
                    type: "time_passed",
                });

            }
        }
        setFormActive(true);
        return;
    }, [config.auto_advance, makeResult]);


    return (
        <div role='trial' className={classNames("aha__trial", config.style)}>
            {playback && (
                <Playback
                    playerType={playback.player_type}
                    instruction={playback.instruction}
                    onPreloadReady={() => {
                        setPreloadReady(true);
                    }}
                    preloadMessage={playback.preload_message}
                    autoAdvance={config.auto_advance}
                    decisionTime={config.decision_time}
                    playConfig={playback.play_config}
                    sections={playback.sections}
                    time={time}
                    submitResult={makeResult}
                    startedPlaying={startTimer}
                    finishedPlaying={finishedPlaying}
                />
            )}
            {preloadReady && feedback_form && (
                <FeedbackForm
                    formActive={formActive}
                    form={feedback_form.form}
                    buttonLabel={feedback_form.submit_label}
                    skipLabel={feedback_form.skip_label}
                    isSkippable={feedback_form.is_skippable}
                    onResult={makeResult}
                    emphasizeTitle={feedback_form.is_profile}
                />
            )}
            {preloadReady && !feedback_form && config.show_continue_button && (
                <div className="text-center">
                    <Button
                        title={config.continue_label}
                        className={
                            "btn-primary anim anim-fade-in anim-speed-500"
                        }
                        onClick={onNext}
                        active={formActive}
                    />
                </div>
            )}
        </div>
    );
};

export default Trial;
