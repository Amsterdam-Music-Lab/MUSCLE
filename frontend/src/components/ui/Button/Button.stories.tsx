/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Button from "./Button";

type Story = StoryObj<typeof Button>;

const meta: Meta<typeof Button> = {
  title: "Design system/Buttons/Button",
  component: Button,
  tags: ["autodocs"],
};
export default meta;

export const Default: Story = {
  args: {
    title: "Click me",
    onClick: () => {},
  },
};

export const VeryLong: Story = {
  args: {
    ...Default.args,
    title: "Lorem ipsum dolor sed amet lorem ipsum dolor sed amet",
  },
};

export const Stretch: Story = {
  args: {
    ...Default.args,
    title: "Stretched link",
    stretch: true,
  },
};

export const Small: Story = {
  args: {
    title: "Small button",
    size: "sm",
  },
};

export const Medium: Story = {
  args: {
    title: "Medium",
    size: "md",
  },
};

export const Large: Story = {
  args: {
    title: "Large",
    size: "lg",
  },
};

export const ExtraLarge: Story = {
  args: {
    title: "Extra large",
    size: "xl",
  },
};

export const Huge: Story = {
  args: {
    title: "Huge!",
    size: "huge",
  },
};

export const NoOutline: Story = {
  args: {
    title: "Large",
    size: "lg",
    outline: false,
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const Hover: Story = {
  args: {
    ...Default.args,
    hover: true,
  },
};

export const WithValue: Story = {
  args: {
    ...Default.args,
    value: "value",
  },
};

export const Secondary = {
  args: {
    ...Default.args,
    variant: "secondary",
  },
};

export const WithOnClick = {
  args: {
    ...Default.args,
    onClick: () => alert("Clicked!"),
  },
};
