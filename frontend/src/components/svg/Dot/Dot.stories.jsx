/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Dot from "./Dot";

export default {
  title: "SVG/Dot",
  component: Dot,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const decorator = (Story) => (
  <div style={{ padding: "1rem" }}>
    <Story />
  </div>
);

export const Default = {
  args: {
    size: 100,
  },
  decorators: [decorator],
};

export const Gradient = {
  args: {
    size: 100,
    fill: { startColor: "#ff0000", endColor: "#0000ff", angle: 30 },
  },
  decorators: [decorator],
};

export const Variant = {
  args: {
    size: 100,
    variant: "primary",
  },
  decorators: [decorator],
};
