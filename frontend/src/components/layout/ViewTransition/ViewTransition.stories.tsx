/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import { useState } from "react";

import ViewTransition from "./ViewTransition";

type Story = StoryObj<typeof ViewTransition>;

const decorator = (StoryComponent: Story) => (
  <div style={{ height: "200px" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof ViewTransition> = {
  title: "App/Layout/ViewTransition",
  component: ViewTransition,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

const pageStyles = {
  width: "100%",
  minHeight: "150px",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  color: "#fff",
};

export const Interactive: Story = {
  render: () => {
    const [page, setPage] = useState(0);
    const colors = ["#e57373", "#64b5f6", "#81c784"];
    return (
      <ViewTransition transitionKey={page}>
        <div style={{ ...pageStyles, background: colors[page] }}>
          <div>
            <h3>Page {page + 1}</h3>
            <button onClick={() => setPage((p) => (p + 1) % colors.length)}>
              Next Page
            </button>
          </div>
        </div>
      </ViewTransition>
    );
  },
};
