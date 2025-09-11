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
};

export const Default = {
  args: {
    score: 100,
    label: "points",
  },
};

export const ZeroScore = {
  args: {
    ...Default.args,
    score: 0,
  },
};

export const NegativeScore = {
  args: {
    ...Default.args,
    score: -100,
  },
};

export const NoScore = {
  args: {
    ...Default.args,
    score: undefined,
  },
};

export const CustomDuration = {
  args: {
    ...Default.args,
    score: 100,
    durationMs: 10000,
  },
};

export const CurstomStartScore = {
  args: {
    ...Default.args,
    score: -100,
    durationMs: 5000,
    startScore: 100,
  },
};

export const ScoreWithoutLabel = {
  args: {
    ...Default.args,
    label: undefined,
  },
};

export const CustomLabel = {
  args: {
    ...Default.args,
    label: "points earned",
  },
};
