/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import ImagePlayer from "./ImagePlayer";
import catImage from "@/assets/images/cat-01.webp";

type Story = StoryObj<typeof ImagePlayer>;

const meta: Meta<typeof ImagePlayer> = {
  title: "Modules/Playback/ImagePlayer",
  component: ImagePlayer,
};

export default meta;

const images = [catImage, "image2.jpg"];

const labels = ["Label 1", "Label 2"];

export const Default: Story = {
  args: {
    images,
    labels,
    playSection: () => {},
    sections: [
      { id: 123, url: "123451" },
      { id: 124, url: "123452" },
    ],
  },
};
