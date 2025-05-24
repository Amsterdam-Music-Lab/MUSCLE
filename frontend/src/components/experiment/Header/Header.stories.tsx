/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";

import Header from "./Header";

type Story = StoryObj<typeof Header>;

const decorator = (StoryComponent: Story) => (
  <div
    className="aha__experiment"
    style={{
      backgroundColor: "#aaa",
      padding: "1rem",
    }}
  >
    <StoryComponent />
  </div>
);

const meta: Meta<typeof Header> = {
  title: "Experiment/Header",
  component: Header,
  decorators: [decorator],
};
export default meta;

export const Default: Story = {
  args: {
    description:
      "<h1>Experiment ABC</h1><p>This is the experiment description</p>",
    nextBlockSlug: "/th1-mozart",
    nextBlockButtonText: "Volgende experiment",
    experimentSlug: "/thkids",
    aboutButtonText: "Over ons",
    totalScore: 420,
    scoreDisplayConfig: {
      scoreClass: "gold",
      scoreLabel: "points",
    },
  },
};

export const ZeroScore: Story = {
  args: {
    ...Default.args,
    totalScore: 0,
    score_message: "No points!",
  },
};

export const NegativeScore: Story = {
  args: {
    ...Default.args,
    totalScore: -100,
  },
};

export const CustomLabel: Story = {
  args: {
    ...Default.args,
    scoreDisplayConfig: { scoreLabel: "points earned" },
  },
};

export const CustomCupType: Story = {
  args: { ...Default.args, scoreDisplayConfig: { scoreClass: "platinum" } },
};
