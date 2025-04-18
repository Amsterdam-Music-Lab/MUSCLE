/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ScoreBoard from "./ScoreBoard";
import { getTimeline } from "../Timeline";

const decorator = (Story) => (
  <div style={{ padding: "1rem", background: "#f5f5f5" }}>
    <Story />
  </div>
);

export default {
  title: "Game UI/ScoreBoard",
  component: ScoreBoard,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

export const Default = {
  args: {
    score: 123,
    totalScore: 456,
    percentile: 48,
  },
  decorators: [decorator],
};

export const BelowCutoff = {
  args: {
    score: 123,
    totalScore: 456,
    percentile: 20,
    percentileCutoff: 25,
  },
  decorators: [decorator],
};

const timeline = getTimeline({
  symbols: [
    "dot",
    "dot",
    "star-4",
    "dot",
    "dot",
    "star-5",
    "dot",
    "dot",
    "star-6",
  ],
});

export const Timeline = {
  args: {
    score: 123,
    totalScore: 456,
    percentile: 59.123,
    timeline: timeline,
    step: 5,
  },
  decorators: [decorator],
};

export const CustomLabels = {
  args: {
    score: 123,
    totalScore: 456,
    percentile: 59,
    timeline: timeline,
    step: 5,
    labels: {
      score: "You've earned points!",
      totalScore: "Total of {{totalScore}} points!",
    },
  },
  decorators: [decorator],
};

export const Sharing = {
  args: {
    score: 123,
    totalScore: 456,
    percentile: 59,
    timeline: timeline,
    step: 5,
    shareConfig: {
      channels: ["facebook", "twitter", "clipboard"],
      url: "https://google.com",
      content: "Test",
      tags: [],
    },
    labels: {
      score: "You've earned points!",
      totalScore: "Total of {{totalScore}} points!",
    },
  },
  decorators: [decorator],
};
