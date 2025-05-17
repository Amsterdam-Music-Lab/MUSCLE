/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ScoreFeedback from "./ScoreFeedback";

export default {
  title: "Game UI/ScoreFeedback",
  component: ScoreFeedback,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const decorator = (Story) => (
  <div style={{ width: "256px", height: "256px", padding: "1rem" }}>
    <Story />
  </div>
);

export const Default = {
  args: {
    turnScore: 10,
    totalScore: 120,
  },
  decorators: [decorator],
};

export const WithMessage = {
  args: {
    turnScore: 10,
    totalScore: 120,
    children: <>You did it!</>,
  },
  decorators: [decorator],
};

export const Centered = {
  args: {
    turnScore: 10,
    totalScore: 120,
    children: <>You did it!</>,
    center: true,
  },
  decorators: [decorator],
};
