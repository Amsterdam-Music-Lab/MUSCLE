/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Cup from "./Cup";

type Story = StoryObj<typeof Cup>;

const meta: Meta<typeof Cup> = {
  title: "Modules/Scoring/Cup",
  component: Cup,
  tags: ["autodocs"],
};

export default meta;

export const Default: Story = {
  args: {},
};

export const Plastic: Story = {
  args: {
    type: "plastic",
  },
};

export const Bronze: Story = {
  args: {
    type: "bronze",
  },
};

export const Silver: Story = {
  args: {
    type: "silver",
  },
};

export const Gold: Story = {
  args: {
    type: "gold",
  },
};

export const Platinum: Story = {
  args: {
    type: "platinum",
  },
};

export const Diamond: Story = {
  args: {
    type: "diamond",
  },
};

export const NoHalo: Story = {
  args: {
    showHalo: false,
  },
};

export const NoAnimation: Story = {
  args: {
    animate: false,
  },
};

export const NoLabel: Story = {
  args: {
    label: false,
  },
};

export const Lowercase: Story = {
  args: {
    uppercase: false,
  },
};

export const CustomLabel: Story = {
  args: {
    label: "Hello and welcome!",
  },
};

export const CustomRadius: Story = {
  args: {
    radius: 300,
  },
};

// export const SilverCup = {
//   args: getRankData({ className: "rank silver" }),
//   decorators: [getDecorator],
// };

// export const BronzeCup = {
//   args: getRankData({ className: "rank bronze" }),
//   decorators: [getDecorator],
// };

// export const NoCupText = {
//   args: getRankData({ text: "" }),
//   decorators: [getDecorator],
// };

// export const ZeroScore = {
//   args: getRankData({ score: 0 }),
//   decorators: [getDecorator],
// };

// export const NegativeScore = {
//   args: getRankData({ score: -100 }),
//   decorators: [getDecorator],
// };

// export const ScoreWithoutLabel = {
//   args: getRankData({ label: "" }),
//   decorators: [getDecorator],
// };

// export const CustomLabel = {
//   args: getRankData({ label: "points earned" }),
//   decorators: [getDecorator],
// };
