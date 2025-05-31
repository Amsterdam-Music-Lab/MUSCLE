/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";

import DashboardHeader from "./DashboardHeader";
import { NarrowLayout } from "@/components/layout";

type Story = StoryObj<typeof Header>;

const decorator = (StoryComponent: Story) => (
  <NarrowLayout>
    <StoryComponent />
  </NarrowLayout>
);

const meta: Meta<typeof Header> = {
  title: "Experiment/DashboardHeader",
  component: DashboardHeader,
  decorators: [decorator],
};
export default meta;

export const Default: Story = {
  args: {
    title: "Experiment ABC",
    description: "This is the experiment description",
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
