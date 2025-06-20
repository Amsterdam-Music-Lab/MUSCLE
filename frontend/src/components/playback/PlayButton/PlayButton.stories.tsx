/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import PlayButton from "./PlayButton";

type Story = StoryObj<typeof PlayButton>;

const meta: Meta<typeof PlayButton> = {
  title: "Modules/Playback/PlayButton",
  component: PlayButton,
};

export default meta;

export const Default: Story = {
  args: {},
};

export const Playing: Story = {
  args: {
    playing: true,
  },
};

export const DisableWhenPlaying: Story = {
  args: {
    playing: true,
    disableWhenPlaying: true,
  },
};

export const OnClick: Story = {
  args: { onClick: () => alert("click!") },
};

// export const BooleanColorScheme: Story = {
//   args: {
//     playing: false,
//     className: "boolean",
//   },
// };

// export const BooleanNegativeFirstColorScheme: Story = {
//   args: {
//     playing: false,
//     className: "boolean-negative-first",
//   },
// };

// export const NeutralColorScheme = {
//   args: {
//     playing: false,
//     className: "neutral",
//   },
// };

// export const NeutralInvertedColorScheme = {
//   args: {
//     playing: false,
//     className: "neutral-inverted",
//   },
// };
