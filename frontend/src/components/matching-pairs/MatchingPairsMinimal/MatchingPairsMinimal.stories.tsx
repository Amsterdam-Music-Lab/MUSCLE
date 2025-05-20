/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import MatchingPairsMinimal from "./MatchingPairsMinimal";

const decorator = (Story) => (
  <div id="root" style={{ padding: "1rem" }}>
    <Story />
  </div>
);

export default {
  title: "Matching Pairs/Matching Pairs Minimal",
  component: MatchingPairsMinimal,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const cards = Array(16)
  .fill(1)
  .map((_, index) => ({
    id: index,
    data: {
      value: index % 8,
    },
  }))
  .sort(() => Math.random() - 0.5);

export const Default = {
  args: { cards: [...cards] },
  decorators: [decorator],
};
