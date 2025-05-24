/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";

import Loading from "./Loading";

type Story = StoryObj<typeof Loading>;

const decorator = (StoryComponent: Story) => (
  <div style={{ height: "300px", background: "#666" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof Loading> = {
  title: "App/Loading",
  component: Loading,
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

export const Default: Story = {
  args: {},
};

export const GapSize: Story = {
  args: { gapSize: 0.5 },
};
