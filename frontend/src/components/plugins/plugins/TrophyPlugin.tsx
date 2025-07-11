/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PluginMeta, PluginSpec } from "@/types/plugin";
import { Trophy, type TrophyProps } from "@/components/modules";

export interface TrophyPluginArgs extends TrophyProps {}

export interface TrophyPluginMeta extends PluginMeta<TrophyPluginArgs> {
  name: "trophy";
}

export interface TrophyPluginSpec extends PluginSpec<TrophyPluginArgs> {
  name: "trophy";
}

export const trophyPlugin: TrophyPluginMeta = {
  name: "trophy",
  component: Trophy,
  description: "Displays a trophy",
  defaultSpecs: {},
};
