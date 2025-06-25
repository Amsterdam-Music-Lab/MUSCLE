/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Autoplay from "./Autoplay";

type Story = StoryObj<typeof Autoplay>;

const decorator = (StoryComponent: Story) => (
  <div style={{ padding: "1rem" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof Autoplay> = {
  title: "Modules/Playback/Autoplay",
  component: Autoplay,
  argTypes: {
    playSection: { action: "playSection" },
    startedPlaying: { action: "startedPlaying" },
    finishedPlaying: { action: "finishedPlaying" },
  },
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

export const Default: Story = {
  args: {
    duration: 100,
    instruction: "Listen to the audio",
  },
};

export const Countdown: Story = {
  args: {
    duration: 50,
    instruction: "Listen to the audio",
    showSpectrum: false,
  },
};

export const Icon: Story = {
  args: {
    ...Default.args,
    showSpectrum: false,
    showCountdown: false,
  },
};

export const LongResponseTime: Story = {
  args: {
    ...Default.args,
    duration: 10000,
  },
};

export const CustomInstruction: Story = {
  args: {
    ...Default.args,
    instruction: "This is a custom instruction for the AutoPlay component",
  },
};
