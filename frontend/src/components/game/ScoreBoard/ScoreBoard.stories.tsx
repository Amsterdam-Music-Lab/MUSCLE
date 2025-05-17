/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ScoreBoard from "./ScoreBoard";

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
    turnScore: 123,
    totalScore: 456,
    percentile: 48,
    timelineStep: 3,
  },
  decorators: [decorator],
};

export const Tunetwins = {
  args: {
    plugins: [
      {
        name: "logo",
        args: { name: "tunetwins", style: { height: "2.5em" } },
        getWrapperProps: () => ({
          style: { display: "flex", justifyContent: "start" },
        }),
      },
      { name: "ranking" },
      { name: "scores" },
      {
        name: "timeline",
        args: {
          timeline: {
            symbols: ["dot", "dot", "star-4", "dot", "dot", "star-5"],
          },
        },
      },
      { name: "share" },
    ],
    turnScore: 123,
    totalScore: 456,
    percentile: 48,
    timelineStep: 3,
    shareConfig: {
      channels: ["facebook", "twitter", "clipboard"],
      url: "https://google.com",
      content: "Test",
      tags: [],
    },
  },
  decorators: [decorator],
};

export const Timeline = {
  args: {
    plugins: [
      { name: "scores" },
      { name: "ranking", order: 1 },
      {
        name: "timeline",
        args: {
          timeline: {
            symbols: ["dot", "dot", "star-4", "dot", "dot", "star-5"],
          },
        },
        order: 0,
      },
      { name: "share" },
    ],
    turnScore: 123,
    totalScore: 456,
    percentile: 48,
    timelineStep: 3,
    shareConfig: {
      channels: ["facebook", "twitter", "clipboard"],
      url: "https://google.com",
      content: "Test",
      tags: [],
    },
  },
  decorators: [decorator],
};

export const BelowCutoff = {
  args: {
    turnScore: 123,
    totalScore: 456,
    percentile: 20,
    plugins: [{ name: "scores" }, { name: "ranking", args: { cutoff: 25 } }],
  },
  decorators: [decorator],
};

export const CustomLabels = {
  args: {
    turnScore: 123,
    totalScore: 456,
    percentile: 59,
    step: 5,
    plugins: [
      { name: "scores" },
      { name: "ranking", order: 1 },
      {
        name: "timeline",
        args: {
          timeline: {
            symbols: ["dot", "dot", "star-4", "dot", "dot", "star-5"],
          },
        },
        order: 0,
      },
      { name: "share" },
    ],
    labels: {
      score: "You've earned points!",
      totalScore: "Total of {{totalScore}} points!",
    },
  },
  decorators: [decorator],
};

export const Sharing = {
  args: {
    turnScore: 123,
    totalScore: 456,
    percentile: 59,
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
