/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import CountDown from "./CountDown";

type Story = StoryObj<typeof CountDown>;

const decorator = (StoryComponent: Story) => (
  <div style={{}}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof CountDown> = {
  title: "UI/CountDown",
  component: CountDown,
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

export const Default: Story = {
  args: {
    duration: 200,
  },
};

export const Paused: Story = {
  args: {
    duration: 200,
    running: false,
  },
};

export const Finished: Story = {
  args: {
    duration: 0,
  },
};
