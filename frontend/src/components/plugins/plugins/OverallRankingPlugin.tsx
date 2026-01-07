/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginMeta, PluginSpec } from "@/types/plugin";
import { t } from "@lingui/core/macro";
import { ProgressBar } from "@/components/ui";

export interface OverallRankingPluginArgs {
  percentile: number;

  totalScore: number;

  /**
   * Message shown above when the percentile is above the cutoff. You can use
   * two variables in the template string: percentile and cutoff
   */
  header?: string;
}

export interface OverallRankingPluginMeta
  extends PluginMeta<OverallRankingPluginArgs> {
  name: "overall-ranking";
}

export interface OverallRankingPluginSpec
  extends PluginSpec<OverallRankingPluginArgs> {
  name: "overall-ranking";
}

function OverallRankingPlugin({ percentile }: OverallRankingPluginArgs) {
  return <ProgressBar value={percentile} variant="secondary" />;
}

function getWrapperProps({ percentile, totalScore }: OverallRankingPluginArgs) {
  percentile = percentile !== undefined ? Math.round(percentile) : "";
  const title = t`Game complete! Your final score is ${totalScore}. That's better than ${percentile}% of players.`;
  return { title, variant: "secondary" };
}

function isVisible({ percentile }: OverallRankingPluginArgs) {
  return typeof percentile === "number" && percentile > 0 && percentile <= 100;
}

export const overallRankingPlugin: OverallRankingPluginMeta = {
  name: "overall-ranking",
  component: OverallRankingPlugin,
  description: "Displays the ranking",
  defaultSpecs: {
    isVisible,
    getWrapperProps,
  },
};
