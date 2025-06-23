/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Card from "./Card";

type Story = StoryObj<typeof Card>;

const decorator = (Story: Story) => (
  <div
    style={{
      minHeight: "300px",
      maxWidth: "400px",
      margin: "auto",
      padding: "1rem",
    }}
  >
    <Story />
  </div>
);

const meta: Meta<typeof Card> = {
  title: "Design system/Layout/Card",
  component: Card,
  tags: ["autodocs"],
  decorators: [decorator],
};
export default meta;

export const Default = {
  args: {
    children: (
      <>
        <Card.Header title="Card title">More content</Card.Header>
        <Card.Section title="Section 1">This is section 1</Card.Section>
        <Card.Section>This is section 2</Card.Section>
      </>
    ),
  },
};

export const Flush = {
  args: {
    children: (
      <>
        <Card.Header title="Card title">More content</Card.Header>
        <Card.Section title="Section 1" flush={true}>
          This is section 1
        </Card.Section>
        <Card.Section>This is section 2</Card.Section>
      </>
    ),
  },
};

export const NarrowSpacing = {
  args: {
    ...Default.args,
    spacing: "narrow",
  },
};

export const NoDividers = {
  args: {
    ...Default.args,
    dividers: false,
  },
};

export const NoDividersNarrow = {
  args: {
    ...Default.args,
    dividers: false,
    spacing: "narrow",
  },
};

export const NoHeader = {
  args: {
    children: (
      <>
        <Card.Section title="Section 1">This is section 1</Card.Section>
        <Card.Section>This is section 2</Card.Section>
      </>
    ),
  },
};

export const CardOptions = {
  args: {
    children: (
      <>
        <Card.Option title="Section 1">This is option 1</Card.Option>
        <Card.Option title="Section 1">This is option 1</Card.Option>
        <Card.Option title="Section 1">This is option 1</Card.Option>
      </>
    ),
  },
};

export const MixedSpacing = {
  args: {
    children: (
      <>
        <Card.Header title="Options">Please select an option</Card.Header>
        <Card.Option spacing="narrow">This is option 1</Card.Option>
        <Card.Option spacing="narrow">This is option 2</Card.Option>
        <Card.Option spacing="narrow">This is option 3</Card.Option>
        <Card.Section title="Ready?">Some footer text...</Card.Section>
      </>
    ),
  },
};
