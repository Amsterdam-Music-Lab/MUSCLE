/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import TypedField from "./TypedField";

type Story = StoryObj<typeof TypedField>;

function TypedFieldControlled({ value: initValue, ...args }) {
  const [value, setValue] = useState(initValue);
  return (
    <TypedField value={value} onChange={(value) => setValue(value)} {...args} />
  );
}

const meta: Meta<typeof TypedField> = {
  title: "Design system/Inputs/Typed Field",
  component: TypedField,
};

export default meta;

export const Default: Story = {
  render: TypedFieldControlled,
  args: {
    placeholder: "Your message goes here...",
    type: "text",
    label: "Your answer",
    required: false,
  },
};

export const Disabled: Story = {
  render: TypedFieldControlled,
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const RequiredDisabled: Story = {
  render: TypedFieldControlled,
  args: {
    ...Default.args,
    required: true,
    disabled: true,
  },
};

export const Icon: Story = {
  render: TypedFieldControlled,
  args: {
    ...Default.args,
    iconName: "globe",
  },
};

export const MaxLength: Story = {
  render: TypedFieldControlled,
  args: {
    ...Default.args,
    maxLength: 20,
  },
};

export const CustomPrefixSuffix: Story = {
  render: TypedFieldControlled,
  args: {
    ...Default.args,
    prefix: "Type:",
    suffix: "Well done",
  },
};

export const Number: Story = {
  render: TypedFieldControlled,
  args: {
    type: "number",
  },
};

export const Email: Story = {
  render: TypedFieldControlled,
  args: {
    type: "email",
  },
};

export const Date: Story = {
  render: TypedFieldControlled,
  args: {
    type: "date",
  },
};

export const URL: Story = {
  render: TypedFieldControlled,
  args: {
    type: "url",
  },
};

export const Error: Story = {
  render: TypedFieldControlled,
  args: {
    ...Default.args,
    error: "This is an error",
  },
};
