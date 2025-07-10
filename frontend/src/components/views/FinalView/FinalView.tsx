/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ScoreBoardProps } from "@/components/modules/ScoreBoard/ScoreBoard";
import type { AllPluginSpec } from "@/components/plugins/pluginRegistry";

import { useEffect } from "react";
import { routes } from "@/config";
import { finalizeSession } from "@/API";
import useBoundStore from "@/util/stores";
import { Final as FinalAction } from "@/types/Action";
import { PluginRenderer } from "@/components/plugins";
import frontendConfig from "@/config/frontend";
import { processTimelineConfig } from "@/components/modules/Timeline/Timeline";
import { TrophyProps } from "@/components/modules";

export type TrophyText = Pick<TrophyProps, "header" | "body">;

export interface TrophyContent {
  first?: TrophyText;
  last?: TrophyText;
  default?: TrophyText;
  [step: number]: TrophyText | undefined;
}

export interface FinalViewProps
  extends FinalAction,
    ScoreBoardProps,
    PluginRendererProps {
  onNext: () => void;
  plugins?: AllPluginSpec[];

  /**
   * The header and body used for the trophy depending on the step size;
   * see documentation of component.
   */
  trophyContent?: TrophyContent;
}

const DEFAULT_PLUGINS = [
  { name: "scoreboard" },
  { name: "linkButton" },
  { name: "userFeedback" },
] as AllPluginSpec[];

/**
 * FinalView shows feedback on the scores in the block, and displays
 * sharing options, and so on. It is a PluginRenderer view, so the
 * content is determined by the plugins passed to the view.
 *
 * In particular, FinalView can show a big trophy, if a timeline is
 * specified and `timeline.currentStep` is a trophy. You can set
 * the exact text messages using the `trophyContent` property. This
 * can set the body and header of the trophy as a function of the
 * step on the timeline:
 *
 * ```ts
 * const trophyContent = {
 *  default: {
 *    header: "Yay, you've earned a star!",
 *    body: "Play on to earn more..."
 *  },
 *
 *  // Special names for the first/last step:
 *  first: { header: "...", body: "..." },
 *  last: { header: "...", body: "..." },
 *
 *  // Or specify the content for a particular step
 *  6: {header: "...", body: "..."},
 * }
 * ```
 */
export default function FinalView({
  block,
  participant,
  action_texts: userLinkTexts,
  button,
  onNext,
  show_participant_link,
  participant_id_only,
  show_profile_link,
  social: shareConfig,
  feedback_info,
  percentile,
  score: turnScore,
  totalScore,
  timeline,
  plugins = frontendConfig?.final?.plugins || DEFAULT_PLUGINS,
  trophyContent = frontendConfig?.final?.trophyContent,
  ...pluginRendererProps
}: FinalViewProps) {
  const session = useBoundStore((state) => state.session);
  useEffect(() => {
    finalizeSession({ session: session!, participant });
  }, [session, participant]);

  // Pass data to plugins
  plugins = plugins?.map((plugin) => {
    const updated: AllPluginSpec = { args: {}, ...plugin };

    switch (plugin.name) {
      case "scoreboard":
        updated.args = {
          ...updated.args,
          turnScore,
          totalScore,
          percentile,
          timeline,
          shareConfig,
        };
        break;

      case "trophy": {
        if (!timeline) return null;

        // If the current step has a trophy, enable the trophy plugin
        const steps = processTimelineConfig({ timeline });
        const step = timeline.currentStep ?? 1;
        const symbol = steps[step - 1]?.symbol ?? "dot";
        const iconName = symbol !== "dot" ? symbol : undefined;
        if (iconName) {
          // Find the right content: first/last or by step number.
          let content;
          const firstTrophyStep =
            steps.findIndex((s) => s.symbol !== "dot") + 1;
          const lastTrophyStep =
            steps.map((s) => s.symbol !== "dot").lastIndexOf(true) + 1;
          if (step === firstTrophyStep) content = trophyContent?.first;
          if (step === lastTrophyStep) content = trophyContent?.last;

          // Otherwise...
          content =
            content ?? trophyContent[step] ?? trophyContent?.default ?? {};
          updated.args = { ...updated.args, iconName, ...content };
        } else {
          return null;
        }
        break;
      }

      case "userPages":
        updated.args = {
          ...updated.args,
          links: [
            {
              link: routes.externalHome(),
              text: userLinkTexts.all_experiments,
            },
            { link: routes.profile(), text: userLinkTexts.profile },
          ],
        };
        break;

      case "userFeedback":
        updated.args = {
          ...updated.args,
          blockSlug: block.slug,
          participant,
          // TODO: cannot yet customize this text...
          feedbackInfo: feedback_info,
        };
        if (!feedback_info) return null;
        break;

      case "participantLink":
        updated.args = {
          ...updated.args,
          participantIDOnly: participant_id_only,
        };
        break;

      case "linkButton":
        updated.args = {
          ...updated.args,
          link: button.link,
          onClick: onNext,
          children: button.text,
        };
        break;
    }

    return updated as AllPluginSpec;
  });

  return (
    <PluginRenderer
      plugins={plugins as AllPluginSpec[]}
      {...pluginRendererProps}
    />
  );
}

FinalView.viewName = "final";
FinalView.usesOwnLayout = false;
FinalView.getViewProps = ({
  block,
  action,
  participant,
  onNext,
  experiment,
}) => {
  const timeline = frontendConfig?.tunetwins?.timeline;
  const numSteps = timeline?.symbols.length ?? timeline?.steps.length ?? 0;
  const sessionsPlayed = experiment.playedSessions ?? 0;
  const timelineStep = (sessionsPlayed % numSteps) + 1;
  console.log(
    "numSteps",
    numSteps,
    "sessions",
    sessionsPlayed,
    "step",
    timelineStep
  );

  return {
    block,
    participant,
    action_texts: action.action_texts,
    button: action.button,
    onNext,
    show_participant_link: action.show_participant_link,
    participant_id_only: action?.participant_id_only,
    show_profile_link: action.show_profile_link,
    social: action.social,
    feedback_info: action.feedback_info,
    percentile: action.percentile,
    score: action.score,
    totalScore: experiment.accumulatedScore + action.score,
    timeline: { ...timeline, currentStep: timelineStep },
  };
};
FinalView.dependencies = ["block", "state", "participant", "onNext"];
