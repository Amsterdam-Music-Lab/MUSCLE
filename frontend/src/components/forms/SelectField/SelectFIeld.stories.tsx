/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import SelectField from "./SelectField";

type Story = StoryObj<typeof SelectField>;

function SelectFieldControlled({ value: initValue, ...args }) {
  const [value, setValue] = useState(initValue);
  return (
    <SelectField
      value={value}
      onChange={(value) => setValue(value)}
      {...args}
    />
  );
}

const meta: Meta<typeof SelectField> = {
  title: "Design system/Inputs/Select Field",
  component: SelectField,
};

export default meta;

export const Default: Story = {
  render: SelectFieldControlled,
  args: {
    value: "jp",
    label: "Country",
    options: [
      {
        value: "nl",
        label: "Netherlands",
      },
      {
        value: "de",
        label: "Germany",
      },
      { value: "uk", label: "United Kingdom" },
      { value: "us", label: "United States" },
      { value: "fr", label: "France" },
      { value: "it", label: "Italy" },
      { value: "jp", label: "Japan" },
      { value: "ch", label: "China" },
      { value: "br", label: "Brazli" },
      { value: "tr", label: "Turkey" },
    ],
    variant: "primary",
  },
};

export const Disabled: Story = {
  render: SelectFieldControlled,
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const Error: Story = {
  render: SelectFieldControlled,
  args: {
    ...Default.args,
    error: "This is an error message",
    showError: true,
  },
};

export const Placeholder: Story = {
  render: SelectFieldControlled,
  args: {
    ...Default.args,
    value: "",
    placeholder: "My placeholder...",
  },
};
