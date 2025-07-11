/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Trophy from "./Trophy";

type Story = StoryObj<typeof Trophy>;

const meta: Meta<typeof Trophy> = {
  title: "Modules/Scoring/Trophy",
  component: Trophy,
  parameters: {
    backgrounds: {
      default: "gray",
      values: [{ name: "gray", value: "#ccc" }],
    },
  },
};

export default meta;

export const Default: Story = {
  args: {
    icon: "star-5",
    header: "Yay, you've won a star!",
    body: "Play on and collect 'm all",
    wobble: true,
    wobbleAngle: 5,
    wobbleDuration: 4000,
  },
};

export const NoConfetti: Story = {
  args: {
    ...Default.args,
    showConfetti: false,
  },
};

export const NoWobble: Story = {
  args: {
    ...Default.args,
    wobble: false,
  },
};
