/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import SmallPlayer from "./SmallPlayer";

type Story = StoryObj<typeof SmallPlayer>;

const decorator = (Story: Story) => (
  <div style={{ maxWidth: "300px" }}>
    <Story />
  </div>
);

const meta: Meta<typeof SmallPlayer> = {
  title: "Playback/SmallPlayer",
  component: SmallPlayer,
  decorators: [decorator],
};

export default meta;

export const Default: Story = {
  args: {
    label: "Some long label.",
  },
};

export const Huge: Story = {
  args: {
    ...Default.args,
    size: "huge",
  },
};

export const OnClick: Story = {
  args: {
    label: "Default",
    onClick: () => alert("Playing"),
  },
};

export const Playing: Story = {
  args: {
    label: "Playing",
    playing: true,
  },
};

export const Disabled: Story = {
  args: {
    label: "Disabled",
    onClick: () => alert("Disabled"),
    disabled: true,
  },
};

export const NotCentered: Story = {
  args: {
    ...Default.args,
    center: false,
  },
};
