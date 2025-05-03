/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginSpec } from "@/components/ui";
import { renderTemplate } from "@/util/renderTemplate";
import { ScoreBar } from "../../ScoreBar";

const DEFAULT_CUTOFF = 30;

interface RankingPluginProps {
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

function RankingPlugin({
  percentile,
  cutoff = DEFAULT_CUTOFF,
}: RankingPluginProps) {
  return (
    <ScoreBar
      value={percentile > cutoff ? percentile : cutoff}
      variant="primary"
    />
  );
}

function getProps({
  percentile,
  cutoff = DEFAULT_CUTOFF,
  headerAboveCutoff = "Congrats! You did better than {{percentile}}% of players at this level",
  headerBelowCuttoff = "Congrats! You did better than {{cutoff}}% of players at this level",
}: RankingPluginProps) {
  return {
    title: renderTemplate(
      percentile > cutoff ? headerAboveCutoff : headerBelowCuttoff,
      {
        percentile: percentile !== undefined ? Math.round(percentile) : "",
        cutoff,
      }
    ),
  };
}

function isVisible({ percentile }: RankingPluginProps) {
  return typeof percentile === "number" && percentile > 0 && percentile <= 100;
}

RankingPlugin._defaults = { getProps, isVisible } as Partial<PluginSpec>;
RankingPlugin._name = "ranking";

export default RankingPlugin;
