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
  tags: ["autodocs"]
};

export const Default = {
  args: {
    score: 123,
    totalScore: 456,
    percentile: 48
  },
  decorators: [decorator]
};

