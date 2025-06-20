/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import MultiPlayer from "./MultiPlayer";

type Story = StoryObj<typeof MultiPlayer>;

const decorator = (Story: Story) => (
  <div style={{ maxWidth: "300px" }}>
    <Story />
  </div>
);

const meta: Meta<typeof MultiPlayer> = {
  title: "Modules/Playback/MultiPlayer",
  component: MultiPlayer,
  decorators: [decorator],
};

export default meta;

const labels = {
  0: "Label 1",
  1: "Label 2",
  2: "Label 3",
  6: "Label 6",
};

export const Default: Story = {
  args: {
    playSection: () => {},
    numSections: 6,
    playerIndex: 0,
    labels,
  },
};

export const DisabledPlayers: Story = {
  args: {
    ...Default.args,
    playerIndex: 2,
    disabledPlayers: [3],
  },
};

const extraContent = {
  5: "Extra Content",
};

export const ExtraContent: Story = {
  args: {
    playSection: () => {},
    numSections: 6,
    playerIndex: "0",
    labels,
    extraContent: (index: number) => extraContent[index],
  },
};
