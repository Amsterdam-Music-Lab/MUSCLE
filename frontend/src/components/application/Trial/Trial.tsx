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

import { useState, useRef, useCallback } from "react";
import { getAudioLatency, getCurrentTime, getTimeSince } from "@/util/time";
import { Playback, View } from "@/components/application";
import { RenderHtml } from "@/components/utils";
import { Button } from "@/components/ui";

export interface TrialProps extends HTMLAttributes<HTMLDivElement> {
  onNext: (breakRound?: boolean) => void;
  onResult: OnResultType;
  playback: PlaybackArgs;
  html: { body: string | TrustedHTML };
  feedback_form: IFeedbackForm;
  config: TrialConfig;
}

/**
 * Trial is a block view to present information to the user and/or collect user feedback
 * If "playback" is provided, it will play audio through the Playback component
 * If "html" is provided, it will show html content
 * If "feedback_form" is provided, it will present a form of questions to the user
 */
export default function Trial({
  playback,
  html,
  feedback_form,
  config,
  onNext,
  onResult,
  experiment,
}: TrialProps) {
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
      if (submitted.current) return;
      submitted.current = true;
      if (!feedback_form) return onNext();

      const { form = [] } = feedback_form;

      if (hasTimedOut) {
        form.map((formElement) => (formElement.value = "TIMEOUT"));
      }

      if (feedback_form.is_skippable) {
        form.map(
          (formElement) => (formElement.value = formElement.value || "")
        );
      }

      const breakRoundConditions = config.break_round_on;
      const shouldBreakRound =
        breakRoundConditions &&
        checkBreakRound(
          form.map((formElement) => formElement.value),
          breakRoundConditions
        );

      await onResult({
        decision_time: getAndStoreDecisionTime(),
        audio_latency_ms: getAudioLatency(),
        form,
        config,
      });

      return onNext(shouldBreakRound);
    },
    [feedback_form, config, onNext, onResult]
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
    if (config.auto_advance) {
      // Create a time_passed result
      if (config.auto_advance_timer != null) {
        if (playback.view === "BUTTON") {
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
    <>
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
          experiment={experiment}
        />
      )}

      {html && <RenderHtml html={html.body} />}

      {preloadReady && feedback_form && (
        <View
          name="survey"
          formActive={formActive}
          form={feedback_form.form}
          buttonLabel={feedback_form.submit_label}
          skipLabel={feedback_form.skip_label}
          isSkippable={feedback_form.is_skippable}
          submitResult={makeResult}
          experiment={experiment}
        />
      )}

      {preloadReady && !feedback_form && config.show_continue_button && (
        <div className="text-center">
          <Button
            title={config.continue_label}
            onClick={onNext}
            disabled={!formActive}
          />
        </div>
      )}
    </>
  );
}

Trial.viewName = "trial";
Trial.usesOwnLayout = true;
Trial.getViewProps = ({ action, onNext, onResult, experiment }) => ({
  playback: action.playback,
  html: action.html,
  feedback_form: action.feedback_form,
  config: action.config,
  onNext,
  onResult,
  experiment,
});
Trial.dependencies = ["action"];
