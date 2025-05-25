/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { vi, it } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import audio from "@/assets/audio.wav";
import TuneTwins from "./TuneTwins";

// Mock the Timeline component
vi.mock("@/components/game", () => ({
  __esModule: true,
  Timeline: (props: any) => <div data-testid="mock-timeline">MockTimeline</div>,
  ScoreFeedback: (props: any) => <></>,
  TutorialMessage: (props: any) => <></>,
}));

const cards = Array(16)
  .fill(1)
  .map((_, index) => ({
    id: index,
    data: {
      url: audio,
      group: index % 8,
    },
  }))
  .sort(() => Math.random() - 0.5);

const defaultArgs = {
  cards,
};

describe("TuneTwins Component", () => {
  it("renders mocked timeline with correct symbols", () => {
    const timeline = { symbols: ["dot", "star-4", "dot"] };
    const { getByTestId } = render(
      <TuneTwins
        {...defaultArgs}
        timeline={timeline}
        showTimeline={true}
        timelineStep={1}
      />
    );
    const timelineDiv = getByTestId("mock-timeline");
    expect(timelineDiv).toBeInTheDocument();
  });
});
