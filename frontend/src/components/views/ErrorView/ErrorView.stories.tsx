/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import { NarrowLayout } from "@/components/layout";
import ErrorView from "./ErrorView";

type Story = StoryObj<typeof ErrorView>;

const decorator = (StoryComponent: Story) => (
  <NarrowLayout>
    <StoryComponent />
  </NarrowLayout>
);

export default {
  title: "App/Views/ErrorView",
  component: ErrorView,
  decorators: [decorator],
} as Meta<typeof ErrorView>;

export const Default = {
  args: {
    message:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  },
};
