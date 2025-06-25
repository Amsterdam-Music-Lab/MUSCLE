/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import InfoView from "./InfoView";

type Story = StoryObj<typeof InfoView>;

const decorator = (StoryComponent: Story) => (
  <div style={{ padding: "4rem", backgroundColor: "#eee" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof InfoView> = {
  title: "App/Views/InfoView",
  component: InfoView,
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

export const Default = {
  args: {
    title: "This is the heading",
    html: "Musica aeterna, harmonia caeli, In sonis veritas, in cantu libertas. Consonantia dulcis, dissonantia audax, Rhythmi vitae, pulsus terrae.",
  },
};

export const WithOnNext = {
  args: {
    ...Default.args,
    onButtonClick: () => alert("Next"),
  },
};

export const WithLink = {
  args: {
    ...Default.args,
    buttonLabel: "Go to some external link",
    buttonLink: "https://www.example.com",
  },
};
