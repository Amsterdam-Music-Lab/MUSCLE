/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import { UserFeedbackForm } from "@/components/user";
import FloatingActionButton from "./FloatingActionButton";
import { UserFeedbackFormProps } from "@/components/user/UserFeedbackForm/UserFeedbackForm";

type Story = StoryObj<typeof FloatingActionButton>;

const decorator = (Story: Story) => (
  <div
    style={{
      width: "100%",
      height: "150px",
      backgroundColor: "#f5f5f5",
    }}
  >
    <Story />
  </div>
);

const meta: Meta<typeof FloatingActionButton> = {
  title: "UI/FloatingActionButton",
  component: FloatingActionButton,
  tags: ["autodocs"],
  decorators: [decorator],
};
export default meta;

export const Default: Story = {
  args: {
    children: <p>The content!</p>,
  },
};

export const TopLeft: Story = {
  args: {
    ...Default.args,
    position: "top-left",
  },
};

export const TopRight: Story = {
  args: {
    ...Default.args,
    position: "top-right",
  },
};

export const BottomLeft: Story = {
  args: {
    ...Default.args,
    position: "bottom-left",
  },
};

export const BottomRight: Story = {
  args: {
    ...Default.args,
    position: "bottom-right",
  },
};

export const CenterLeft: Story = {
  args: {
    ...Default.args,
    position: "center-left",
  },
};

export const CenterRight: Story = {
  args: {
    ...Default.args,
    position: "center-right",
  },
};

export const FlushRight: Story = {
  args: {
    ...Default.args,
    position: "center-right",
    flush: true,
  },
};

export const FlushLeft: Story = {
  args: {
    ...FlushRight.args,
    position: "center-left",
  },
};

export const VariantSecondary: Story = {
  args: {
    ...Default.args,
    variant: "secondary",
  },
};

const userFeedbackProps: UserFeedbackFormProps = {
  blockSlug: "test",
  participant: "test",
  feedbackInfo: {
    header: "Feedback",
    button: "Submit",
    thank_you: "Thank you for your feedback!",
    contact_body:
      '<p>Please contact us at <a href="mailto:info@example.com">info@example.com</a> if you have any questions.</p>',
    show_float_button: false, // ignored?
  },
  inline: false,
};

export const Feedback: Story = {
  args: {
    ...Default.args,
    title: "Your Feedback",
    wrapInCardSection: false,
    children: <UserFeedbackForm wrapInCard={false} {...userFeedbackProps} />,
  },
};

export const CustomOffsetFontSize: Story = {
  args: {
    ...Default.args,
    position: "top-left",
    fontSize: 3,
    offset: 4,
  },
};
