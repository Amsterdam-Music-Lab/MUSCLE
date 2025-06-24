/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import TextAreaField from "./TextAreaField";

type Story = StoryObj<typeof TextAreaField>;

function TextAreaFieldControlled({ value: initValue, ...args }) {
  const [value, setValue] = useState(initValue);
  return (
    <TextAreaField
      value={value}
      onChange={(value) => setValue(value)}
      {...args}
    />
  );
}

const meta: Meta<typeof TextAreaField> = {
  title: "Design system/Inputs/TextArea Field",
  component: TextAreaField,
};

export default meta;

export const Default: Story = {
  render: TextAreaFieldControlled,
  args: {
    placeholder: "Start writing your essay...",
    label: "Why do you think people should eat more carrots?",
  },
};

export const Disabled: Story = {
  render: TextAreaFieldControlled,
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const Error: Story = {
  render: TextAreaFieldControlled,
  args: {
    ...Default.args,
    error: "This is an error message",
    showError: true,
  },
};

export const LongResizable: Story = {
  render: TextAreaFieldControlled,
  args: {
    ...Default.args,
    rows: 10,
    resizable: true,
  },
};
