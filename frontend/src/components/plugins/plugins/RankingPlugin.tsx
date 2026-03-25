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
  finalText: string;
  extraInfo: string;
}

export interface RankingPluginMeta extends PluginMeta<RankingPluginArgs> {
  name: "ranking";
}

export interface RankingPluginSpec extends PluginSpec<RankingPluginArgs> {
  name: "ranking";
}

function RankingPlugin({
  percentile,
  finalText,
  extraInfo,
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
  finalText,
  extraInfo,
  cutoff = DEFAULT_CUTOFF,
}: RankingPluginArgs) {
  const title = finalText;
  const caption = extraInfo;
  return { title, caption };
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
