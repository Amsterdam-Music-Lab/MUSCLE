import { useState, useRef, useCallback } from "react";
import classNames from "classnames";

import { getCurrentTime, getTimeSince } from "../../util/time";
import FeedbackForm from "../FeedbackForm/FeedbackForm";
import HTML from "../HTML/HTML";
import Playback from "../Playback/Playback";
import Button from "../Button/Button";
import Question from "@/types/Question";
import { OnResultType } from "@/hooks/useResultHandler";
import { TrialConfig } from "@/types/Trial";

interface IFeedbackForm {
    form: Question[];
    submit_label: string;
    skip_label: string;
    is_skippable: boolean;
}

interface TrialProps {
    playback: any;
    html: { body: string | TrustedHTML };
    feedback_form: IFeedbackForm;
    config: TrialConfig;
    result_id: string;
    onNext: (breakRound?: boolean) => void;
    onResult: OnResultType;
}

/**
 * Trial is an block view to present information to the user and/or collect user feedback
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
        result_id,
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
        async (result: { type: 'time_passed' }) => {
            // Prevent multiple submissions
            if (submitted.current) {
                return;
            }
            submitted.current = true;

            // TODO: Check if we can find another solution for
            // the default value of form than [{}]
            const form = feedback_form ? feedback_form.form : [{}];

            if (result.type === "time_passed") {
                form.map((formElement) => (formElement.value = "TIMEOUT"));
            }

            if (feedback_form) {

                if (feedback_form.is_skippable) {
                    form.map((formElement => (formElement.value = formElement.value || '')))
                }

                const breakRoundOn = config.break_round_on;
                const shouldBreakRound = breakRoundOn && checkBreakRound(form.map((formElement) => formElement.value), breakRoundOn);
                const shouldCallOnNextInOnResult = !shouldBreakRound

                await onResult(
                    {
                        decision_time: getAndStoreDecisionTime(),
                        form,
                        config
                    },
                    false,
                    // if we break the round, we don't want to call onNext in onResult
                    shouldCallOnNextInOnResult
                );

                if (shouldBreakRound) {
                    onNext(true);
                }

            } else {
                if (result_id) {
                    onResult({
                        result,
                        result_id
                    });
                } else {
                    onNext();
                }

            }
        },
        [feedback_form, config, onNext, onResult, result_id]
    );

    const checkBreakRound = (values, breakConditions) => {
        switch (Object.keys(breakConditions)[0]) {
            case 'EQUALS':
                return values.some(val => breakConditions['EQUALS']
                    .includes(val));
            case 'NOT':
                return !values.some(val => breakConditions['NOT'].includes(val));
            default:
                return false;
        }

    }

    const getAndStoreDecisionTime = () => {
        const decisionTime = getTimeSince(startTime.current);
        // keep decisionTime in sessionStorage to be used by subsequent renders
        window.sessionStorage.setItem('decisionTime', decisionTime);
        return decisionTime;
    }

    const finishedPlaying = useCallback(() => {

        if (config.auto_advance) {

            // Create a time_passed result
            if (config.auto_advance_timer != null) {
                if (playback.view === 'BUTTON') {
                    startTime.current = getCurrentTime();
                }

                setTimeout(() => { makeResult({ type: "time_passed", }); }, config.auto_advance_timer);
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
                        disabled={!formActive}
                    />
                </div>
            )}
        </div>
    );
};

export default Trial;
