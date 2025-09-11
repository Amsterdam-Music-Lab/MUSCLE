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

const DEFAULT_CUTOFF = 30;

export interface RankingPluginArgs {
  percentile: number;
  cutoff: number;

  /**
   * Message shown above when the percentile is above the cutoff. You can use
   * two variables in the template string: percentile and cutoff
   */
  headerAboveCutoff?: string;

  /**
   * Message shown above when the percentile is below the cutoff. You can use
   * two variables in the template string: percentile and cutoff
   */
  headerBelowCuttoff?: string;
}

export interface RankingPluginMeta extends PluginMeta<RankingPluginArgs> {
  name: "ranking";
}

export interface RankingPluginSpec extends PluginSpec<RankingPluginArgs> {
  name: "ranking";
}

function RankingPlugin({
  percentile,
  cutoff = DEFAULT_CUTOFF,
}: RankingPluginArgs) {
  return (
    <ProgressBar
      value={percentile > cutoff ? percentile : cutoff}
      variant="primary"
    />
  );
}

function getWrapperProps({
  percentile,
  cutoff = DEFAULT_CUTOFF,
}: RankingPluginArgs) {
  percentile = percentile !== undefined ? Math.round(percentile) : "";
  const title =
    percentile > cutoff
      ? t`Congrats! You did better than ${percentile}% of players at this level`
      : t`Congrats! You did better than ${cutoff}% of players at this level`;
  return { title };
}

function isVisible({ percentile }: RankingPluginArgs) {
  return typeof percentile === "number" && percentile > 0 && percentile <= 100;
}

export const rankingPlugin: RankingPluginMeta = {
  name: "ranking",
  component: RankingPlugin,
  description: "Displays the ranking",
  defaultSpecs: {
    isVisible,
    getWrapperProps,
  },
};
