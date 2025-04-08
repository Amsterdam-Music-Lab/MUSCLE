/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ScoreBar from "./ScoreBar";

const decorator = (Story) => (
  <div style={{ padding: "1rem", background: "#f5f5f5" }}>
      <Story />
  </div>
);

export default {
  title: "UI/ScoreBar",
  component: ScoreBar,
  parameters: {
      layout: "fullscreen",
  },
  tags: ["autodocs"]
};


export const Default = {
  args: {
    value: 80,
  },
  decorators: [decorator]
};


export const DifferentRange = {
  args: {
    min: -50,
    max: 250,
    value: 80,
    template: "{{value}} points"
  },
  decorators: [decorator]
};

export const NoAnimation = {
  args: {
    animate: false,
    value: 20
  },
  decorators: [decorator]
}