/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ScoreFeedback from "./ScoreFeedback";

export default {
  title: "Modules/Scoring/ScoreFeedback",
  component: ScoreFeedback,
};

export const Default = {
  args: {
    turnScore: 10,
    totalScore: 120,
  },
};

export const WithMessage = {
  args: {
    ...Default.args,
    children: <>You did it!</>,
  },
};

export const Centered = {
  args: {
    ...WithMessage.args,
    center: true,
  },
};
