/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import ScoreBoard from "./ScoreBoard";

type Story = StoryObj<typeof ScoreBoard>;

const decorator = (StoryComponent: Story) => (
  <div style={{ padding: "1rem" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof ScoreBoard> = {
  title: "Game UI/ScoreBoard",
  component: ScoreBoard,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

export const Default: Story = {
  args: {
    turnScore: 123,
    totalScore: 456,
    percentile: 48,
    timelineStep: 3,
  },
};

const defaultPlugins = [
  {
    name: "logo",
    args: { name: "tunetwins", style: { height: "2.5em" } },
    getWrapperProps: () => ({
      style: { display: "flex", justifyContent: "start" },
    }),
  },
  { name: "ranking" },
  { name: "scores" },
  {
    name: "timeline",
    args: {
      timeline: {
        symbols: ["dot", "dot", "star-4", "dot", "dot", "star-5"],
      },
    },
  },
  {
    name: "markdown",
    args: { content: "This is custom *markdown* content." },
    getWrapperProps: () => ({
      title: "Markdown!",
    }),
  },
  { name: "share" },
];

export const BelowCutoff: Story = {
  args: {
    turnScore: 123,
    totalScore: 456,
    percentile: 20,
    plugins: [{ name: "ranking", args: { cutoff: 25 } }, { name: "scores" }],
  },
};

export const CustomPlugins: Story = {
  args: {
    plugins: defaultPlugins,
    turnScore: 123,
    totalScore: 456,
    percentile: 48,
    timelineStep: 3,
    shareConfig: {
      channels: ["facebook", "twitter", "clipboard"],
      url: "https://google.com",
      content: "Test",
      tags: [],
    },
  },
};
