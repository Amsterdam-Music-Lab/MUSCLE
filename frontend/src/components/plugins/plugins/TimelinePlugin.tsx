/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PluginMeta, PluginSpec } from "@/types/plugin";
import Timeline, {
  type TimelineProps,
} from "@/components/game/Timeline/Timeline";

export interface TimelinePluginArgs extends TimelineProps {}

export interface TimelinePluginMeta extends PluginMeta<TimelinePluginArgs> {
  name: "timeline";
}

export interface TimelinePluginSpec extends PluginSpec<TimelinePluginArgs> {
  name: "timeline";
}

export const timelinePlugin: TimelinePluginMeta = {
  name: "timeline",
  component: Timeline,
  description: "Displays an timeline",
  defaultSpecs: {},
};
