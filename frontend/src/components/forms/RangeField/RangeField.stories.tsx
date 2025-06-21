/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";
import RangeField from "./RangeField";
import SliderField from "./SliderField";
import IconSliderField from "./IconSliderField";

type Story = StoryObj<typeof RangeField>;

const decorator = (Story: Story) => <Story />;

function RangeFieldControlled({ value: initValue, ...args }) {
  const [value, setValue] = useState(initValue);
  return (
    <RangeField
      values={value}
      onChange={(values) => setValue(values)}
      {...args}
    />
  );
}

function SliderFieldControlled({ value: initValue, ...args }) {
  const [value, setValue] = useState(initValue);
  return (
    <SliderField
      value={value}
      onChange={(value) => setValue(value)}
      {...args}
    />
  );
}

const meta: Meta<typeof RangeField> = {
  title: "Design system/Inputs/Range Field",
  component: RangeField,
  decorators: [decorator],
};

export default meta;

export const Default: Story = {
  render: RangeFieldControlled,
  args: {
    min: 0,
    max: 100,
    step: 10,
    showTicks: true,
    showTickLabels: true,
    autoTickLabels: true,
    showIntermediateTickLabels: true,
    variant: "primary",
  },
};

export const Likert: Story = {
  render: RangeFieldControlled,
  args: {
    value: ["agree"],
    options: [
      { value: "strongly_disagree", label: "strongly disagree" },
      { value: "disagree", label: "disagree" },
      { value: "neutral", label: "neither agree nor disagree" },
      { value: "agree", label: "agree" },
      { value: "strongly_agree", label: "strongly agree" },
    ],
  },
};

export const LikertNoInitialValue: Story = {
  render: RangeFieldControlled,
  args: {
    ...Likert.args,
    initialPosition: 2,
    value: undefined,
    options: [
      { value: "strongly_disagree", label: "strongly disagree" },
      { value: "disagree", label: "disagree" },
      { value: "neutral", label: "neither agree nor disagree" },
      { value: "agree", label: "agree" },
      { value: "strongly_agree", label: "strongly agree" },
    ],
  },
};

export const LabelsInside: Story = {
  render: RangeFieldControlled,
  args: {
    ...Default.args,
    showTickLabelsInside: true,
    thumbSize: "2.5em",
  },
};

export const Disabled: Story = {
  render: RangeFieldControlled,
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const Error: Story = {
  render: RangeFieldControlled,
  args: {
    ...Default.args,
    error: "An error occured.",
  },
};

export const Slider: Story = {
  render: SliderFieldControlled,
  args: {
    ...Likert.args,
    value: "agree",
  },
};

const iconClasses = [
  "fa-face-grin-hearts",
  "fa-face-grin",
  "fa-face-smile",
  "fa-face-meh",
  "fa-face-frown",
  "fa-face-frown-open",
  "fa-face-angry",
];

export const IconSlider: Story = {
  render: SliderFieldControlled,
  args: {
    options: iconClasses.map((icon) => ({
      value: icon,
      label: <span className={`fa ${icon}`} style={{ fontSize: "2em" }} />,
    })),
    showIntermediateTickLabels: true,
    showTickLabelsInside: true,
    thumbSize: "3.5em",
  },
};
