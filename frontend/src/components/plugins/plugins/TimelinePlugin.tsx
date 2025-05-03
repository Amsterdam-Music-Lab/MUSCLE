/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PluginMeta, PluginSpec } from "@/types/plugin";
import Timeline, {
  getTimeline,
  type GetTimelineProps,
  type TimelineProps,
} from "@/components/game/Timeline/Timeline";

export interface TimelinePluginArgs extends GetTimelineProps, TimelineProps {}

export interface TimelinePluginMeta extends PluginMeta<TimelinePluginArgs> {
  name: "timeline";
}

export interface TimelinePluginSpec extends PluginSpec<TimelinePluginArgs> {
  name: "timeline";
}

function TimelinePlugin({
  symbols,
  dotSize,
  trophySize,
  animate,
  showDots,
  step,
  variant = "primary",
  showSpine = true,
  timeline,
  ...timelineProps
}: TimelinePluginArgs) {
  if (!timeline)
    timeline = getTimeline({
      symbols,
      dotSize,
      trophySize,
      animate,
      showDots,
    });
  return (
    <Timeline
      timeline={timeline}
      step={step + 1}
      variant={variant}
      showSpine={showSpine}
      {...timelineProps}
    />
  );
}

export const timelinePlugin: TimelinePluginMeta = {
  name: "timeline",
  component: TimelinePlugin,
  description: "Displays an timeline",
  defaultSpecs: {},
};
