/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { StoryObj } from "@storybook/react";
import PluginCard from "./PluginCard";

// type Story = StoryObj<typeof Card>;

export default {
  title: "UI/PluginCard",
  component: PluginCard,
  tags: ["autodocs"],
  decorators: [
    (Story) => (
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

const Title = ({ title, description }) => <p>Description: {description}</p>;

const components = {
  title: Title,
};

export const Default = {
  args: {
    plugins: [
      {
        name: "title",
        title: "Whatever",
        args: { title: "bla", description: "boe" },
      },
      {
        name: "title",
        propsFn: (args) => ({
          title: `Title: ${args.title}`,
        }),
        args: { title: "Another title", description: "boe" },
        title: "Blabla",
      },
    ],
    components,
  },
};
