/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { PluginSpec } from "@/components/ui";
import Timeline, {
  getTimeline,
  type GetTimelineProps,
  type TimelineProps,
} from "../../Timeline/Timeline";

interface TimelinePluginProps extends GetTimelineProps, TimelineProps {}

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
}: TimelinePluginProps) {
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

TimelinePlugin._defaults = {} as Partial<PluginSpec>;
TimelinePlugin._name = "timeline";

export default TimelinePlugin;
