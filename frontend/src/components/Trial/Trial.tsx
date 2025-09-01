import { useState, useRef, useCallback } from "react";
import classNames from "classnames";

import { getCurrentTime, getTimeSince } from "@/util/time";
import FeedbackForm from "../FeedbackForm/FeedbackForm";
import HTML from "../HTML/HTML";
import Playback from "../Playback/Playback";
import Button from "../Button/Button";
import { OnResultType } from "@/hooks/useResultHandler";
import { TrialConfig } from "@/types/Trial";
import { Trial as TrialAction } from "@/types/Action";

export interface TrialProps extends TrialAction {
    onNext: (breakRound?: boolean) => void;
    onResult: OnResultType;
}

/**
 * Trial is a block view to present information to the user and/or collect user feedback
 * If "playback" is provided, it will play audio through the Playback component
 * If "html" is provided, it will show html content
 * If "feedback_form" is provided, it will present a form of questions to the user
 */
const Trial = (props: TrialProps) => {

    const {
        playback,
        html,
        feedback_form,
        config,
        onNext,
        onResult,
    } = props;

    // Main component state
    const [formActive, setFormActive] = useState(!config.listen_first);
    // Preload is immediately set to ready if we don't have a playback object
    const [preloadReady, setPreloadReady] = useState(!playback);

    const submitted = useRef(false);

    // This is used to keep track of the time a participant spends in this Trial view
    const startTime = useRef(getCurrentTime());

    const startTimer = useCallback(() => {
        startTime.current = getCurrentTime();
    }, []);

    // Create result data
    const makeResult = useCallback(
        async (hasTimedOut: boolean) => {

            // Prevent multiple submissions
            if (submitted.current) {
                return;
            }
            submitted.current = true;

            if (!feedback_form) {
                return onNext();
            }


            const { form = [] } = feedback_form;

            if (hasTimedOut) {
                form.map((formElement) => (formElement.value = "TIMEOUT"));
            }

            if (feedback_form.is_skippable) {
                form.map((formElement => (formElement.value = formElement.value || '')))
            }

            const breakRoundConditions = config.break_round_on;
            const shouldBreakRound = breakRoundConditions && checkBreakRound(form.map((formElement) => formElement.value), breakRoundConditions);

            await onResult(
                {
                    decision_time: getAndStoreDecisionTime(),
                    audio_latency_ms: getAudioLatency(),
                    form,
                    config,
                },
            );

            return onNext(shouldBreakRound);

        },
        [feedback_form, config, onNext, onResult]
    );

    const checkBreakRound = (
        values: string[],
        breakConditions: TrialConfig['break_round_on']
    ) => {
        switch (Object.keys(breakConditions)[0]) {
            case 'EQUALS':
                return values
                    .some(
                        val => breakConditions['EQUALS']!.includes(val)
                    );
            case 'NOT':
                return !values.some(
                    val => breakConditions['NOT']!.includes(val)
                );
            default:
                return false;
        }

    }

    const getAndStoreDecisionTime = () => {
        const decisionTime = getTimeSince(startTime.current);
        // keep decisionTime in sessionStorage to be used by subsequent renders
        window.sessionStorage.setItem('decisionTime', decisionTime.toString());
        return decisionTime;
    }

    const getAudioLatency = () => {
        if (window.sessionStorage.getItem('audioLatency') !== null) {
            return window.sessionStorage.getItem('audioLatency');
        } else {
            return NaN;
        }
    }

    const finishedPlaying = useCallback(() => {

        if (config.auto_advance) {

            // Create a time_passed result
            if (config.auto_advance_timer != null) {
                if (playback.view === 'BUTTON') {
                    startTime.current = getCurrentTime();
                }

                setTimeout(() => {
                    makeResult(true);
                }, config.auto_advance_timer);
            } else {
                makeResult(true);
            }
        }
        setFormActive(true);
        return;
    }, [config, playback, makeResult]);

    return (
        <div role="presentation" className={classNames("aha__trial", config.style)}>
            {playback && (
                <Playback
                    playbackArgs={playback}
                    onPreloadReady={() => {
                        setPreloadReady(true);
                    }}
                    autoAdvance={config.auto_advance}
                    responseTime={config.response_time}
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
                    submitResult={makeResult}
                />
            )}
            {preloadReady && !feedback_form && config.show_continue_button && (
                <div className="text-center">
                    <Button
                        title={config.continue_label}
                        className={"btn-primary anim anim-fade-in anim-speed-500"}
                        onClick={onNext}
                        disabled={!formActive}
                    />
                </div>
            )}
        </div>
    );
};

export default Trial;
