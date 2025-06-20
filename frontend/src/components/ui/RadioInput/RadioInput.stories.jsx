/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import RadioInput from "./RadioInput";

const decorator = (Story) => (
  <div style={{ width: "100%", height: "100%", padding: "1rem" }}>
    <Story />
  </div>
);
export default {
  title: "Design system/Inputs/RadioInput",
  component: RadioInput,
  decorators: [decorator],
};

export const Default = {
  args: {
    values: ["Option 1", "Option 2", "Option 3"],
  },
};

export const Selected = {
  args: {
    values: ["Option 1", "Option 2", "Option 3"],
    value: "Option 2",
  },
};

export const CustomLabels = {
  args: {
    values: ["opt1", "opt2", "opt3", "opt4"],
    labels: ["Label 1", "Label 2", "Label 3", "Label 4"],
    value: "opt2",
  },
};
