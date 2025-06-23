/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import CheckboxField from "./CheckboxField";
import RadioField from "./RadioField";
import OptionField from "./OptionField";

type CheckboxStory = StoryObj<typeof CheckboxField>;
type RadioStory = StoryObj<typeof RadioField>;
type Story = CheckboxStory | RadioStory;

const decorator = (Story: Story) => <Story />;

function CheckboxFieldControlled({ value: initValue, ...args }) {
  const [value, setValue] = useState(initValue);
  return (
    <CheckboxField
      value={value}
      onChange={(values) => setValue(values)}
      {...args}
    />
  );
}

function RadioFieldControlled({ value: initValue, ...args }) {
  const [value, setValue] = useState(initValue);
  return (
    <RadioField
      value={value}
      onChange={(values) => setValue(values)}
      {...args}
    />
  );
}

const meta: Meta<typeof CheckboxFieldControlled> = {
  title: "Design system/Inputs/Option Field",
  component: OptionField,
  decorators: [decorator],
};

export default meta;

export const Checkboxes: CheckboxStory = {
  render: CheckboxFieldControlled,
  args: {
    name: "fruit",
    value: ["banana"],
    options: [
      { value: "apple", label: "Apple" },
      { value: "banana", label: "Banana" },
      { value: "cherry" },
      { value: "dragonfruit", label: "Dragonfruit!", disabled: true },
    ],
    label: "Pick your favourite fruit!",
  },
};

export const Radios: RadioStory = {
  render: RadioFieldControlled,
  args: {
    ...Checkboxes.args,
    value: "banana",
  },
};

export const Disabled: CheckboxStory = {
  render: CheckboxFieldControlled,
  args: {
    ...Checkboxes.args,
    disabled: true,
  },
};

export const Errors: CheckboxStory = {
  render: CheckboxFieldControlled,
  args: {
    ...Checkboxes.args,
    error: "There is something wrong with your selection.",
  },
};
