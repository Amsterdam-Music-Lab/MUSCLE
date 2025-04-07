/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ScoreDisplay from "./ScoreDisplay";

const decorator = (Story) => (
  <div style={{ padding: "1rem", background: "#f5f5f5" }}>
      <Story />
  </div>
);

export default {
  title: "Game UI/ScoreDisplay",
  component: ScoreDisplay,
  parameters: {
      layout: "fullscreen",
  },
  tags: ["autodocs"]
};

export const Default = {
  args: {
    score: 321,
    label: "Your score"
  },
  decorators: [decorator]
};


export const ExtraLarge = {
  args: {
    score: 321,
    label: "Your score",
    units: "points",
    size: 6
  },
  decorators: [decorator]
};

export const NoScore = {
  args: {
    label: "Your score",
  },
  decorators: [decorator]
};


export const NegativeScore = {
  args: {
    score: -200,
    label: "Another score",
  },
  decorators: [decorator]
};

export const HTMLAttributes = {
  args: {
    score: -200,
    label: "Another score",
    style: { background: "#fff", padding: "1em"  },
  },
  decorators: [decorator]
};
