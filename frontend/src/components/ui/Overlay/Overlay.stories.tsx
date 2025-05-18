/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Overlay from "./Overlay";

const meta: Meta<typeof Overlay> = {
  title: "UI/Overlay",
  component: Overlay,
  tags: ["autodocs"],
};

export default meta;
type Story = StoryObj<typeof Overlay>;

export const Default: Story = {
  args: {
    open: false,
    title: "Tutorial",
    children: "This is a tutorial.",
    onClose: () => {},
  },
};

export const Open: Story = {
  args: {
    ...Default.args,
    open: true,
  },
};

export const WithLongContent: Story = {
  args: {
    ...Default.args,
    children: (
      <div>
        <h3>Welcome to our app!</h3>
        <p>Here's how to get started:</p>
        <ol>
          <li>First, create your profile</li>
          <li>Then, explore our features</li>
          <li>Finally, start creating!</li>
        </ol>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </p>
      </div>
    ),
  },
};

export const CustomTitle: Story = {
  args: {
    ...Default.args,
    title: "🎉 Getting Started",
    children: "Welcome to our awesome app!",
  },
};
