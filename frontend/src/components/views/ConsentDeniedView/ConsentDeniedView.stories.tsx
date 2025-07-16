/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import { NarrowLayout } from "@/components/layout";
import ConsentDeniedView from "./ConsentDeniedView";

type Story = StoryObj<typeof ConsentDeniedView>;

const decorator = (StoryComponent: Story) => (
  <NarrowLayout>
    <StoryComponent />
  </NarrowLayout>
);

export default {
  title: "App/Views/ConsentDeniedView",
  component: ConsentDeniedView,
  decorators: [decorator],
} as Meta<typeof ConsentDeniedView>;

export const Default = {
  args: {},
};
