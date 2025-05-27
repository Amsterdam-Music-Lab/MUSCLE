/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import type { ScoreBoardProps } from "@/components/game/ScoreBoard/ScoreBoard";
import type { AllPluginSpec } from "@/components/plugins/pluginRegistry";

import { useEffect } from "react";
import { URLS } from "@/config";
import { finalizeSession } from "@/API";
import useBoundStore from "@/util/stores";
import { Final as FinalAction } from "@/types/Action";
import { NarrowLayout } from "@/components/layout";
import { PluginRenderer } from "@/components/plugins";
import frontendConfig from "@/config/frontend";

export interface FinalViewProps
  extends FinalAction,
    ScoreBoardProps,
    HTMLAttributes<HTMLDivElement> {
  onNext: () => void;
  plugins?: AllPluginSpec[];
}

const DEFAULT_PLUGINS = [
  { name: "scoreboard" },
  { name: "linkButton" },
  { name: "userFeedback" },
] as AllPluginSpec[];

/**
 * Final is a block view that shows the final scores of the block
 * It can only be the last view of a block
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
  totalScore, // TODO
  timeline, // TODO
  timelineStep = 0, // TODO
  plugins = frontendConfig?.final?.plugins || DEFAULT_PLUGINS,
  ...layoutProps
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
          timelineStep,
          shareConfig,
        };
        break;

      case "userPages":
        updated.args = {
          ...updated.args,
          links: [
            { link: URLS.AMLHome, text: userLinkTexts.all_experiments },
            { link: URLS.profile, text: userLinkTexts.profile },
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
    <NarrowLayout {...layoutProps}>
      <PluginRenderer plugins={plugins as AllPluginSpec[]} />
    </NarrowLayout>
  );
}
