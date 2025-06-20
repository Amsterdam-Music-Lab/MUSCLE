/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import type { TrialConfig } from "@/types/Trial";
import type { IFeedbackForm } from "@/types/Action";
import type { PlaybackArgs } from "@/types/Playback";
import type { OnResultType } from "@/hooks/useResultHandler";
import type SurveyQuestion from "@/types/Question";

import { useState, useRef, useEffect, useCallback } from "react";
import { getAudioLatency, getCurrentTime, getTimeSince } from "@/util/time";
import { Playback, View } from "@/components/application";
import { RenderHtml } from "@/components/utils";
import { Button } from "@/components/ui";

export interface Survey {
  /** The questions to show */
  questions: SurveyQuestion[];

  /** Whether the survey can be skipped */
  skippable?: boolean;

  /** Label for the submit button */
  submitLabel?: string;

  /** Label for the skip button */
  skipLabel?: string;
}

export interface TrialProps extends HTMLAttributes<HTMLDivElement> {
  onNext: (breakRound?: boolean) => void;
  onResult: OnResultType;
  playback: PlaybackArgs;
  html: { body: string | TrustedHTML };
  survey: Survey;
  responseTime: number;
  autoAdvance: boolean;
  listenFirst: boolean;
  breakRoundOn: BreakRoundOn;
  autoAdvanceTimer: number | null;

  /** Whether to show the continue button. */
  showContinueButton: boolean;

  /** Label for the continue button. Default "Continue" */
  continueLabel?: string;
}

/**
 * Trial is a block view to present information to the user and/or collect user feedback
 * If "playback" is provided, it will play audio through the Playback component
 * If "html" is provided, it will show html content
 * If "survey" is provided, it will present a form of questions to the user
 */
export default function Trial({
  playback,
  html,
  survey,
  onNext,
  onResult,
  experiment,
  responseTime,
  autoAdvance,
  autoAdvanceTimer,
  listenFirst,
  breakRoundOn,
  showContinueButton,
  continueLabel = "Continue",
}: TrialProps) {
  // Preload is immediately set to ready if we don't have a playback object
  const [preloadReady, setPreloadReady] = useState(!playback);
  const [disableSurvey, setDisableSurvey] = useState(listenFirst);
  const [questions, setQuestions] = useState(survey?.form ?? []);
  console.log(questions);
  // Update state whenever the props change. This ensures the Trial is
  // rerendered when moving to the next question in a round, for example.
  useEffect(() => {
    setQuestions(survey?.questions ?? []);
  }, [survey?.questions]);

  // Track the time a participant spends in this Trial view
  const startTime = useRef(getCurrentTime());
  const startTimer = useCallback(() => {
    startTime.current = getCurrentTime();
  }, []);

  const handleSubmit = useCallback(
    async (hasTimedOut: boolean, updatedQuestions: IFeedbackForm["form"]) => {
      // Continue if there's no form
      if (!survey) return onNext();

      // If the for has timed out, flag all questions as TIMEOUT
      if (hasTimedOut) updatedQuestions.forEach((q) => (q.value = "TIMEOUT"));

      // Set empty values for skipped questions
      if (survey.skippable)
        updatedQuestions.forEach((q) => (q.value = q.value || ""));

      const values = updatedQuestions.map((q) => q.value);
      const shouldBreakRound =
        breakRoundOn && checkBreakRound(values, breakRoundOn);

      // Submit to server
      const result = await onResult({
        decision_time: getAndStoreDecisionTime(),
        audio_latency_ms: getAudioLatency(),
        form: updatedQuestions,
        config: {
          response_time: responseTime,
          auto_advance: autoAdvance,
          auto_advance_timer: autoAdvanceTimer,
          listen_first: listenFirst,
          show_continue_button: showContinueButton,
          continue_label: continueLabel,
          break_round_on: breakRoundOn,
        },
      });
      if (!result?.success)
        console.warn("The survey could not be submitted", result);

      return onNext(shouldBreakRound);
    },
    [
      survey,
      breakRoundOn,
      responseTime,
      autoAdvance,
      autoAdvanceTimer,
      listenFirst,
      showContinueButton,
      continueLabel,
      onNext,
      onResult,
    ]
  );

  const checkBreakRound = (
    values: string[],
    breakConditions: TrialConfig["break_round_on"]
  ) => {
    switch (Object.keys(breakConditions)[0]) {
      case "EQUALS":
        return values.some((val) => breakConditions["EQUALS"]!.includes(val));
      case "NOT":
        return !values.some((val) => breakConditions["NOT"]!.includes(val));
      default:
        return false;
    }
  };

  const getAndStoreDecisionTime = () => {
    const decisionTime = getTimeSince(startTime.current);
    // keep decisionTime in sessionStorage to be used by subsequent renders
    window.sessionStorage.setItem("decisionTime", decisionTime.toString());
    return decisionTime;
  };

  const finishedPlaying = useCallback(() => {
    if (autoAdvance) {
      // Create a time_passed result
      if (autoAdvanceTimer != null) {
        if (playback.view === "BUTTON") {
          startTime.current = getCurrentTime();
        }

        setTimeout(() => {
          handleSubmit(true, questions);
        }, autoAdvanceTimer);
      } else {
        handleSubmit(true, questions);
      }
    }
    setDisableSurvey(false);
    return;
  }, [questions, autoAdvance, autoAdvanceTimer, playback, handleSubmit]);

  return (
    <>
      {playback && (
        <Playback
          playbackArgs={playback}
          onPreloadReady={() => setPreloadReady(true)}
          autoAdvance={autoAdvance}
          responseTime={responseTime}
          submitResult={(hasTimedOut) => handleSubmit(hasTimedOut, questions)}
          startedPlaying={startTimer}
          finishedPlaying={finishedPlaying}
          experiment={experiment}
        />
      )}

      {html && <RenderHtml html={html.body} />}

      {preloadReady && survey && (
        <View
          name="survey"
          questions={questions}
          onChange={setQuestions}
          onSubmit={(updatedSurvey) => handleSubmit(undefined, updatedSurvey)}
          disabled={disableSurvey}
          skippable={survey.skippable}
          submitLabel={survey.submitLabel}
          skipLabel={survey.skipLabel}
        />
      )}

      {preloadReady && !survey && showContinueButton && (
        <div className="text-center">
          <Button
            title={continueLabel}
            onClick={onNext}
            disabled={disableSurvey}
          />
        </div>
      )}
    </>
  );
}

Trial.viewName = "trial";
Trial.usesOwnLayout = true;
Trial.getViewProps = ({ action, onNext, onResult, experiment }) => {
  let survey;
  if (action.feedback_form) {
    survey = {
      questions: action.feedback_form?.form,
      skippable: action.feedback_form?.is_skippable,
      submitLabel: action.feedback_form?.submit_label,
      skipLabel: action.feedback_form?.skip_label,
    };
  }

  return {
    playback: action.playback,
    html: action.html,
    survey,
    onNext,
    onResult,
    experiment,
    responseTime: action.config.response_time,
    autoAdvance: action.config.auto_advance,
    autoAdvanceTimer: action.config.auto_advance_timer,
    listenFirst: action.config.listen_first,
    showContinueButton: action.config.show_continue_button,
    continueLabel: action.config.continue_label,
    breakRoundOn: action.config.break_round_on,
  };
};
Trial.dependencies = ["action"];
