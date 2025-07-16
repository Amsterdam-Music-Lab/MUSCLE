/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { Variant } from "@/types/themeProvider";

import { useLingui } from "@lingui/react/macro";
import ScoreDisplay from "@/components/modules/ScoreDisplay/ScoreDisplay";

interface ScoresPluginProps {
  turnScore?: number;
  totalScore?: number;
  turnScoreLabel?: string;
  totalScoreLabel?: string;
  variant?: Variant;
}

function ScoresPlugin({
  turnScore,
  totalScore,
  turnScoreLabel,
  totalScoreLabel,
  variant = "secondary",
}: ScoresPluginProps) {
  const { t } = useLingui();
  return (
    <div style={{ display: "flex" }}>
      <div style={{ width: "50%" }}>
        <ScoreDisplay
          score={turnScore}
          label={turnScoreLabel ?? t`Last game`}
          variant={variant}
        />
      </div>
      <div style={{ width: "50%" }}>
        <ScoreDisplay
          score={totalScore}
          label={totalScoreLabel ?? t`Total score`}
          variant={variant}
        />
      </div>
    </div>
  );
}

export interface ScoresPluginArgs extends ScoresPluginProps {}

export interface ScoresPluginMeta extends PluginMeta<ScoresPluginArgs> {
  name: "scores";
}

export interface ScoresPluginSpec extends PluginSpec<ScoresPluginArgs> {
  name: "scores";
}

export const scoresPlugin: ScoresPluginMeta = {
  name: "scores",
  component: ScoresPlugin,
  description: "Displays the turn and total score",
};
