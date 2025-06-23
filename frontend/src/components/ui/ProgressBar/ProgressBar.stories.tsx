/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ProgressBar from "./ProgressBar";

const decorator = (Story) => (
  <div style={{ padding: "1rem" }}>
    <Story />
  </div>
);

export default {
  title: "Design System/Feedback/ProgressBar",
  component: ProgressBar,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

export const Default = {
  args: {
    value: 80,
  },
  decorators: [decorator],
};

export const NegativeRange = {
  args: {
    min: -50,
    max: 250,
    value: 80,
    template: "{{value}} points",
  },
  decorators: [decorator],
};

export const PositiveRange = {
  args: {
    min: 50,
    max: 150,
    value: 80,
    template: "{{value}} points",
  },
  decorators: [decorator],
};

export const NoAnimation = {
  args: {
    animate: false,
    value: 20,
  },
  decorators: [decorator],
};

export const NoVariant = {
  args: {
    value: 40,
    variant: null,
  },
  decorators: [decorator],
};

export const PrimaryVariant = {
  args: {
    value: 40,
    variant: "primary",
  },
  decorators: [decorator],
};

export const SecondaryVariant = {
  args: {
    value: 40,
    variant: "secondary",
  },
  decorators: [decorator],
};
