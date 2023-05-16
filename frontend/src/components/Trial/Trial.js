import React, { useState, useRef, useCallback } from "react";
import classNames from "classnames";

import { getCurrentTime, getTimeSince } from "../../util/time";
import FeedbackForm from "../FeedbackForm/FeedbackForm";
import HTML from "../HTML/HTML";
import Playback from "../Playback/Playback";
import Button from "../Button/Button";

/** Trial is an experiment view to present information to the user and/or collect user feedback
If "playback" is provided, it will play audio through the Playback component
If "html" is provided, it will show html content
If "feedback_form" is provided, it will present a form of questions to the user
**/
const Trial = ({
    playback,
    html,
    feedback_form,
    config,
    result_id,
    onNext,
    onResult,
}) => {
    // Main component state
    const [formActive, setFormActive] = useState(!config.listen_first);
    const [preloadReady, setPreloadReady] = useState(!playback?.play_config?.ready_time);

    const submitted = useRef(false);

    // This is used to keep track of the time a participant spends in this Trial view
    const startTime = useRef(getCurrentTime());

    // Time ref, stores the time without updating the view
    const time = useRef(0);
    const startTimer = useCallback(() => {
        startTime.current = getCurrentTime();
    }, []);

    // Create result data
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
                if (feedback_form.is_skippable) {
                    form.map((formElement => (formElement.value = formElement.value || '')))
                }
                onResult({
                    decision_time,
                    form,
                    config
                });
            } else {
                onResult({
                    result,
                    result_id
                })
            }
        },
        [feedback_form, config, onNext, onResult]
    );

    const finishedPlaying = useCallback(() => {

        if (config.auto_advance) {

            // Create a time_passed result
            if (config.auto_advance_timer != null) {
                if (playback.player_type === 'BUTTON') {
                    startTime.current = getCurrentTime();
                }

            } else {

                makeResult({
                    type: "time_passed",
                });

            }
        }
        setFormActive(true);
        return;
    }, [config, playback, makeResult]);


    return (
        <div role="presentation" className={classNames("aha__trial", config.style)}>
            {playback && (
                <Playback
                    playerType={playback.player_type}
                    instruction={playback.instruction}
                    onPreloadReady={() => {
                        setPreloadReady(true);
                    }}
                    preloadMessage={playback.preload_message}
                    autoAdvance={config.auto_advance}
                    responseTime={config.response_time}
                    playConfig={playback.play_config}
                    sections={playback.sections}
                    time={time}
                    submitResult={makeResult}
                    startedPlaying={startTimer}
                    finishedPlaying={finishedPlaying}
                />
            )}
            {html && (
                <HTML
                    body={html.body}
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
                    // emphasizeTitle={feedback_form.is_profile}
                    // to do: if we want left-aligned text with a pink divider,
                    // make this style option available again (used in Question.scss)
                />
            )}
            {preloadReady && !feedback_form && config.show_continue_button && (
                <div className="text-center">
                    <Button
                        title={config.continue_label}
                        className={"btn-primary anim anim-fade-in anim-speed-500"}
                        onClick={onNext}
                        active={formActive}
                    />
                </div>
            )}
        </div>
    );
};

export default Trial;
