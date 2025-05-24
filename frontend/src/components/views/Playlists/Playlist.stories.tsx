/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { Meta, StoryObj } from "@storybook/react";
import Playlists from "./Playlists";

type Story = StoryObj<typeof InPlaylistfo>;

const decorator = (StoryComponent: Story) => (
  <div style={{ padding: "2rem" }}>
    <StoryComponent />
  </div>
);

const meta: Meta<typeof Playlists> = {
  title: "views/Playlists",
  component: Playlists,
  tags: ["autodocs"],
  decorators: [decorator],
};

export default meta;

const playlists = [
  { id: "42", name: "Playlist A" },
  { id: "43", name: "Playlist B" },
  { id: "44", name: "Playlist C" },
  { id: "45", name: "Playlist D" },
];

export const Default = {
  args: {
    title: "Select a playlist...",
    playlists,
    instruction: "This is an elaborate instruction",
    onNext: () => {},
    playlist: { current: "42" },
  },
};

export const NoAnimation = {
  args: {
    ...Default.args,
    animate: false,
  },
};
