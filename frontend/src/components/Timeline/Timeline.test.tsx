/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { describe, test, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders.tsx";
import Timeline, { processTimelineConfig } from "./Timeline.tsx";
import { TimelineConfig } from "@/types/timeline.ts";

describe("Timeline component", () => {
  const timeline = {
    steps: ["", "", "str", ""],
    playedSessions: 2,
    dotSize: 10,
    trophySize: 20,
    animate: true,
  } as TimelineConfig;

  test("renders symbols and spine segments", () => {
    const { container } = render(<Timeline timeline={timelineConfig} />);
    const steps = container.querySelectorAll(`.aha__timeline-symbol`);
    expect(steps).toHaveLength(4);
    const spines = container.querySelectorAll(`aha__timeline-spine-segment`);
    expect(spines).toHaveLength(3);
  });

});
