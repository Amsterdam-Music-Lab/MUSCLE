/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ScoreDisplay from "./ScoreDisplay";

export default {
  title: "Modules/Scoring/ScoreDisplay",
  component: ScoreDisplay,
};

export const Default = {
  args: {
    score: 321,
    label: "Your score",
  },
};

export const ExtraLarge = {
  args: {
    score: 321,
    label: "Your score",
    units: "points",
    size: 6,
  },
};

export const NoScore = {
  args: {
    label: "Your score",
  },
};

export const ZeroScore = {
  args: {
    label: "Your score",
    score: 0,
  },
};

export const NegativeScore = {
  args: {
    score: -200,
    label: "Another score",
  },
};

export const HTMLAttributes = {
  args: {
    score: -200,
    label: "Another score",
    style: { background: "#fff", padding: "1em" },
  },
};

export const NoVariant = {
  args: {
    score: -200,
    variant: null,
  },
};

export const PrimaryVariant = {
  args: {
    score: -200,
    variant: "primary",
  },
};

export const SecondaryVariant = {
  args: {
    score: -200,
    variant: "secondary",
  },
};

export const Centered = {
  args: {
    score: 1234,
    label: "My very long label is even longer now",
    center: true,
  },
};
