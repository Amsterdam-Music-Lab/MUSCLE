import { useState, useRef, useCallback } from "react";
import classNames from "classnames";

import { getCurrentTime, getTimeSince } from "@/util/time";
import FeedbackForm from "../FeedbackForm/FeedbackForm";
import HTML from "../HTML/HTML";
import Playback from "../Playback/Playback";
import Button from "../Button/Button";
import { OnResultType } from "@/hooks/useResultHandler";
import { ITrial } from "@/types/Action";
import Theme from "@/types/Theme";
import { BreakRoundOn } from "@/types/Trial";

export interface TrialProps extends ITrial {
    onNext: (breakRound?: boolean) => void;
    onResult: OnResultType;
    theme: Theme;
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
        feedbackForm,
        responseTime,
        listenFirst,
        autoAdvance,
        continueButton,
        breakRoundOn,
        onNext,
        onResult,
    } = props;

    // Main component state
    const [formActive, setFormActive] = useState(playback? !listenFirst: true);
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
        async (hasTimedOut?: boolean) => {

            // Prevent multiple submissions
            if (submitted.current) {
                return;
            }
            submitted.current = true;

            if (!feedbackForm) {
                return onNext();
            }


            const { form = [] } = feedbackForm;

            if (hasTimedOut) {
                form.map((formElement) => (formElement.value = "TIMEOUT"));
            }

            if (feedbackForm.skipButton) {
                form.map((formElement => (formElement.value = formElement.value || '')))
            }

            const breakRoundConditions = breakRoundOn;
            const shouldBreakRound = breakRoundConditions && checkBreakRound(form.map((formElement) => formElement.value), breakRoundConditions);

            await onResult(
                {
                    decision_time: getAndStoreDecisionTime(),
                    audio_latency_ms: getAudioLatency(),
                    form,
                },
            );
            return onNext(shouldBreakRound);

        },
        [feedbackForm, onNext, onResult]
    );

    const checkBreakRound = (
        values: string[],
        breakConditions: BreakRoundOn
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
        if (autoAdvance) {

            // Create a time_passed result
            if (playback.view === 'BUTTON') {
                startTime.current = getCurrentTime();
                if (responseTime) {
                    // create timeout result after responseTime
                    setTimeout(() => {
                        makeResult(true);
                    }, responseTime * 1000);
                }
            } else {
                makeResult(true);
            }
        }
        setFormActive(true);
        return;
    }, [autoAdvance, responseTime, playback, makeResult]);

    return (
        <div role="presentation" className={classNames("aha__trial")}>
            {playback && (
                <Playback
                    {...playback}
                    onPreloadReady={() => {
                        setPreloadReady(true);
                    }}
                    autoAdvance={autoAdvance}
                    responseTime={responseTime}
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
            {preloadReady && feedbackForm && (
                <FeedbackForm
                    formActive={formActive}
                    form={feedbackForm.form}
                    submitButton={feedbackForm.submitButton}
                    skipButton={feedbackForm.skipButton}
                    submitResult={makeResult}
                />
            )}
            {preloadReady && !feedbackForm && continueButton && (
                <div className="text-center">
                    <Button
                        {...continueButton}
                        className={"anim anim-fade-in anim-speed-500"}
                        onClick={onNext}
                        disabled={!formActive}
                    />
                </div>
            )}
        </div>
    );
};

export default Trial;
