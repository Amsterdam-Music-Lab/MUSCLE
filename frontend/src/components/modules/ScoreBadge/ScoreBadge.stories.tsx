/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import ScoreBadge from "./ScoreBadge";

type Story = StoryObj<typeof ScoreBadge>;

const meta: Meta<typeof ScoreBadge> = {
  title: "Modules/Scoring/ScoreBadge",
  component: ScoreBadge,
};

export default meta;

export const Default: Story = {};
