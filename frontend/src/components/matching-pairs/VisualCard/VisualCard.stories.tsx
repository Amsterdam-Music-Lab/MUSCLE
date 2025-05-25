/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import VisualCard from "./VisualCard";
import catImage from "@/assets/images/cat-01.webp";

export default {
  title: "Matching Pairs/VisualCard",
  component: VisualCard,
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
  args: {
    src: `http://localhost:6006${catImage}`,
    alt: "Image of a cat",
  },
  decorators: [decorator],
};

export const Front = {
  args: {
    src: `http://localhost:6006${catImage}`,
    alt: "Image of a cat",
    flipped: true,
  },
  decorators: [decorator],
};

export const MissingImage = {
  args: {
    src: `http://localhost:6006/bla`,
    alt: "A nonexistent image",
    flipped: true,
  },
  decorators: [decorator],
};
