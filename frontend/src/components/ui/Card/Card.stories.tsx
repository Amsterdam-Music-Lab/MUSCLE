/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { StoryObj } from "@storybook/react";
import Card from "./Card";

type Story = StoryObj<typeof Card>;

export default {
  title: "UI/Card",
  component: Card,
  tags: ["autodocs"],
  decorators: [
    (Story: Story) => (
      <div
        style={{
          width: "100%",
          height: "300px",
          padding: "1rem",
          background: "#eee",
        }}
      >
        <div style={{ width: "300px", margin: "auto" }}>
          <Story />
        </div>
      </div>
    ),
  ],
};

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
