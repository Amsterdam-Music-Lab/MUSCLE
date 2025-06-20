/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ScoreCounter from "./ScoreCounter";

export default {
  title: "Modules/Scoring/ScoreCounter",
  component: ScoreCounter,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

function getScoreData(overrides = {}) {
  return {
    score: 100,
    label: "points",
    ...overrides,
  };
}

const getDecorator = (Story) => (
  <div
    style={{
      backgroundColor: "#eee",
      padding: "1rem",
    }}
  >
    <Story />
  </div>
);

export const Default = {
  args: getScoreData(),
  decorators: [getDecorator],
};

export const ZeroScore = {
  args: getScoreData({ score: 0 }),
  decorators: [getDecorator],
};

export const NegativeScore = {
  args: getScoreData({ score: -100 }),
  decorators: [getDecorator],
};

export const NoScore = {
  args: getScoreData({ score: undefined }),
  decorators: [getDecorator],
};

export const CustomDuration = {
  args: getScoreData({ score: 100, durationMs: 10000 }),
  decorators: [getDecorator],
};

export const CurstomStartScore = {
  args: getScoreData({ score: -100, durationMs: 5000, startScore: 100 }),
  decorators: [getDecorator],
};

export const ScoreWithoutLabel = {
  args: getScoreData({ label: undefined }),
  decorators: [getDecorator],
};

export const CustomLabel = {
  args: getScoreData({ label: "points earned" }),
  decorators: [getDecorator],
};
