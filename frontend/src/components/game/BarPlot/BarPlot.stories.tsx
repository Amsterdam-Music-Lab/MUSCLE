/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import BarPlot from "./BarPlot";

const decorator = (Story) => (
  <div style={{ padding: "1rem", height: "300px", maxWidth: "200px", margin: "auto" }}>
      <Story />
  </div>
);

export default {
  title: "Game UI/BarPlot",
  component: BarPlot,
  parameters: {
      layout: "fullscreen",
  },
  tags: ["autodocs"]
};


export const Default = {
  args: {
    data: [30, 40, 80, 40, 10, 20],
    min: 0,
    max: 100
  },
  decorators: [decorator]
};

export const TwoBars = {
  args: {
    data: [30,80],
    min: 0,
    max: 100
  },
  decorators: [decorator]
};


export const ManyBars = {
  args: {
    data: [30, 0, 80, 10, 40, 50, 60, 90, 100, 2, 50, 30, 40, 80, 10, 40, 50, 60, 90, 100, 2, 50],
    min: 0,
    max: 100
  },
  decorators: [decorator]
};

export const Color = {
  args: {
    data: [30, 40, 80, 40, 10, 20],
    min: 0,
    max: 100,
    color: "red"
  },
  decorators: [decorator]
};

export const SecondaryVariant = {
  args: {
    data: [30, 40, 80, 40, 10, 20],
    min: 0,
    max: 100,
    variant: "secondary"
  },
  decorators: [decorator]
};