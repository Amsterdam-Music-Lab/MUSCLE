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
        args: { symbols: ["dot", "dot", "star-4", "dot", "dot", "star-5"] },
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
        args: { symbols: ["dot", "dot", "star-4", "dot", "dot", "star-5"] },
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
    percentileCutoff: 25,
  },
  decorators: [decorator],
};

// const timeline = getTimeline({
//   symbols: [
//     "dot",
//     "dot",
//     "star-4",
//     "dot",
//     "dot",
//     "star-5",
//     "dot",
//     "dot",
//     "star-6",
//   ],
// });

// export const Timeline = {
//   args: {
//     score: 123,
//     totalScore: 456,
//     percentile: 59.123,
//     timeline: timeline,
//     step: 5,
//   },
//   decorators: [decorator],
// };

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
        args: { symbols: ["dot", "dot", "star-4", "dot", "dot", "star-5"] },
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
/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { PluginMeta, PluginSpec } from "@/types/plugin";
import type { Variant } from "@/types/themeProvider";

import ScoreDisplay from "@/components/game/ScoreDisplay/ScoreDisplay";

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

export interface ScoresPluginArgs extends ScoresPluginProps {}

export interface ScoresPluginMeta extends PluginMeta<ScoresPluginArgs> {
  name: "scores";
}

export interface ScoresPluginSpec extends PluginSpec<ScoresPluginArgs> {
  name: "scores";
}

export const scoreboardPlugin: ScoresPluginMeta = {
  name: "scores",
  component: ScoresPlugin,
  description: "Displays the turn and total score",
};
