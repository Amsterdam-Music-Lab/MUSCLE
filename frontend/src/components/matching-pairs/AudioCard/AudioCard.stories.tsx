/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import AudioCard from "./AudioCard";

type Story = StoryObj<typeof AudioCard>;

const decorator = (StoryComponent: Story) => (
  <div style={{ width: "200px", height: "200px" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof AudioCard> = {
  title: "Matching Pairs/AudioCard",
  component: AudioCard,
  decorators: [decorator],
};

export default meta;

export const Back = {
  args: {},
};

export const Front = {
  args: {
    flipped: true,
  },
  decorators: [decorator],
};

export const Playing = {
  args: {
    flipped: true,
    running: true,
  },
  decorators: [decorator],
};
