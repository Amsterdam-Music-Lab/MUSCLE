/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import RenderHtml from "./RenderHtml";

type Story = StoryObj<typeof HTML>;

const decorator = (StoryComponent: Story) => (
  <div style={{ margin: "2em", backgroundColor: "#fafafa" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof HTML> = {
  title: "App/RenderHtml",
  component: RenderHtml,
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

export const Default: Story = {
  args: {
    html: "<div>Hello world</div>",
  },
};

export const Prose: Story = {
  args: {
    html: `<div class="prose">
        <h1>Title</h1>
        <p>Paragraph <strong>with bold text</strong></p>
        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
        </ul>
      </div>`,
  },
};

export const Card: Story = {
  args: {
    html: `
      <div class="card bg-blue">
        <div class="card-title">Title</div>
        <div class="card-text">Hello world!</div>
      </div>`,
  },
};
