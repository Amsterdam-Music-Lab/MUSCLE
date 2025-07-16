/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import { NarrowLayout } from "@/components/layout";
import AboutView from "./AboutView";

type Story = StoryObj<typeof AboutView>;

const decorator = (StoryComponent: Story) => (
  <NarrowLayout>
    <StoryComponent />
  </NarrowLayout>
);

export default {
  title: "App/Views/AboutView",
  component: AboutView,
  decorators: [decorator],
} as Meta<typeof AboutView>;

export const Default = {
  args: {
    content:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  },
};
