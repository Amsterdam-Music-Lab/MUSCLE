/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { ScoreBoardProps } from "@/components/game/ScoreBoard/ScoreBoard";
import ScoreBoard from "@/components/game/ScoreBoard/ScoreBoard";

interface ScoreboardPluginArgs extends ScoreBoardProps {}

export interface ScoreboardPluginMeta extends PluginMeta<ScoreboardPluginArgs> {
  name: "scoreboard";
}

export interface ScoreboardPluginSpec extends PluginSpec<ScoreboardPluginArgs> {
  name: "scoreboard";
}

export const scoreboardPlugin: ScoreboardPluginMeta = {
  name: "scoreboard",
  component: ScoreBoard,
  description: "Displays an scoreboard",
  defaultSpecs: {},
};
