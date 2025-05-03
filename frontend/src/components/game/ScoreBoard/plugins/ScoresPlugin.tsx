/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginSpec } from "@/components/ui";
import { ScoreDisplay } from "../../ScoreDisplay";
import { Variant } from "@/types/themeProvider";

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
  turnScoreLabel = "Last game",
  totalScoreLabel = "Total score",
  variant = "secondary",
}: ScoresPluginProps) {
  return (
    <div className="d-flex">
      <div style={{ width: "50%" }}>
        <ScoreDisplay
          score={turnScore}
          label={turnScoreLabel}
          variant={variant}
        />
      </div>
      <div style={{ width: "50%" }}>
        <ScoreDisplay
          score={totalScore}
          label={totalScoreLabel}
          variant={variant}
        />
      </div>
    </div>
  );
}

ScoresPlugin._defaults = {} as Partial<PluginSpec>;
ScoresPlugin._name = "scores";

export default ScoresPlugin;
