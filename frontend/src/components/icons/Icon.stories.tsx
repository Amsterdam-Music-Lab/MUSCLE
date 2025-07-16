/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Icon from "./Icon";

type Story = StoryObj<typeof Icon>;

const meta: Meta<typeof Icon> = {
  title: "Design System/SVG/Icon",
  component: Icon,
  parameters: {
    backgrounds: {
      values: [{ value: "#ddd" }],
    },
  },
};

export default meta;

export const Default: Story = {
  args: {
    name: "facebook",
    // fill: "#f00",
  },
};

export const CustomColor: Story = {
  args: {
    ...Default.args,
    fill: "#f00",
  },
};

export const Size: Story = {
  args: {
    name: "share",
    size: "6em",
  },
};
