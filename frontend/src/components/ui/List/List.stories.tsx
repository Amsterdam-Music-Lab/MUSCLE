/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import List from "./List";

type Story = StoryObj<typeof List>;

const meta: Meta<typeof List> = {
  title: "Design system/Layout/List",
  component: List,
};
export default meta;

export const Default: Story = {
  args: {
    items: [
      { content: "Item 1" },
      { content: "Item 2" },
      { content: "Item 3" },
    ],
    animate: true,
    delay: 250,
  },
};

export const NoAnimation: Story = {
  args: {
    ...Default.args,
    animate: false,
  },
};

export const CustomLabels: Story = {
  args: {
    ...Default.args,
    items: [
      { label: "A", content: "Item 1" },
      { label: "B", content: "Item 2" },
      { label: "C", content: "Item 3" },
    ],
  },
};

export const Unordered: Story = {
  args: {
    ...Default.args,
    ordered: false,
  },
};

export const Markdown: Story = {
  args: {
    ...Default.args,
    items: [
      { content: "Item 1, with some **bold** text" },
      { label: "B", content: "Item 2" },
      { label: "C", content: "Item 3" },
    ],
  },
};
