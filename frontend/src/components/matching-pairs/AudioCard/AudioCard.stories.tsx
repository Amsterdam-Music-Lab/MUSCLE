/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import AudioCard from "./AudioCard";

export default {
  title: "Matching Pairs/AudioCard",
  component: AudioCard,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const decorator = (Story) => (
  <div style={{ width: "256px", height: "256px", padding: "1rem" }}>
    <Story />
  </div>
);

export const Back = {
  args: {},
  decorators: [decorator],
};

export const Front = {
  args: {
    flipped: true,
  },
  decorators: [decorator],
};
