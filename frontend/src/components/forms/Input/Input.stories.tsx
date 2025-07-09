/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Input from "./Input";

const decorator = (Story) => (
  <div
    style={{
      height: "100%",
      padding: "1rem",
      background: "#eee",
    }}
  >
    <Story />
  </div>
);

export default {
  title: "Design System/Inputs/Input",
  component: Input,
  tags: ["autodocs"],
  decorators: [decorator],
};

export const Default = {
  args: {
    value: "A test value",
  },
};

export const Placeholder = {
  args: {
    placeholder: "Your name",
  },
};

export const ReadOnly = {
  args: {
    readOnly: true,
    value: "A test value",
  },
};
