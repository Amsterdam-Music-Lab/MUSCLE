/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Meta, StoryObj } from "@storybook/react";
import FieldWrapper from "./FieldWrapper";

type Story = StoryObj<typeof FieldWrapper>;

const meta: Meta<typeof FieldWrapper> = {
  title: "Design system/Inputs/FieldWrapper",
  component: FieldWrapper,
};

export default meta;

const MockInput = (props) => <input type="text" {...props} />;

export const Default: Story = {
  args: {
    name: "test",
    label: "Please type something",
    children: <MockInput />,
  },
};

export const Error: Story = {
  args: {
    ...Default.args,
    error: "An error occured!",
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const Required: Story = {
  args: {
    ...Default.args,
    required: true,
  },
};

export const RequiredDisabled: Story = {
  args: {
    ...Required.args,
    ...Disabled.args,
  },
};

export const RequiredDisabledError: Story = {
  args: {
    ...Required.args,
    ...Disabled.args,
    ...Error.args,
  },
};

export const CustomConfig: Story = {
  args: {
    ...RequiredDisabledError.args,
    disabledText: "Sorry, I'm disabled!",
    showErrorIcon: false,
    showLabel: true,
    showRequired: true,
    showDisabled: true,
  },
};
