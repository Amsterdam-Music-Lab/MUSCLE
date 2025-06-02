/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Background from "./Background";

type Story = StoryObj<typeof Background>;

const decorator = (StoryComponent: Story) => (
  <div style={{ height: "200px" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof Background> = {
  title: "App/Background",
  component: Background,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

export const Default: Story = {
  args: {},
};

export const NoGradientCircles: Story = {
  args: {
    showGradientCircles: false,
  },
};
