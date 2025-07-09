/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import "@testing-library/jest-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import { vi, describe, it, expect } from "vitest";
import PlaylistsView from "./PlaylistsView";

vi.mock("@/util/stores");

describe("PlaylistsView Component", () => {
  const curPlaylist = { current: "42" };
  const playlists = [
    { id: "42", name: "Playlist A" },
    { id: "43", name: "Playlist B" },
  ];
  const onSelect = vi.fn();

  it("renders correctly with given props", () => {
    render(
      <PlaylistsView
        playlist={curPlaylist}
        playlists={playlists}
        instruction="instruction"
        onSelect={onSelect}
      />
    );
    expect(screen.getByText("instruction")).toBeInTheDocument();
    const playlistItems = screen.getAllByTestId("playlist-item");
    expect(playlistItems.length === 2);
  });

  it("calls onNext when playlist item is clicked", () => {
    render(
      <PlaylistsView
        playlists={playlists}
        playlist={curPlaylist}
        instruction="instruction"
        onSelect={onSelect}
      />
    );
    fireEvent.click(screen.getAllByTestId("playlist-item")[0]);
    expect(onSelect).toHaveBeenCalled();
  });

  it("does not render with less than 2 playlists", () => {
    render(
      <PlaylistsView
        playlists={[{ id: "42", name: "Playlist A" }]}
        playlist={curPlaylist}
        instruction="instruction"
        onSelect={onSelect}
      />
    );
    expect(onSelect).toHaveBeenCalled();
    expect(screen.queryByTestId("playlist-instruction")).toBeNull();
  });
});
