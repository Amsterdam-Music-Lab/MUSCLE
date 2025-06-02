/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { CardProps } from "@/components/ui";
import type { MutableRefObject } from "react";
import type { Playlist } from "@/types/Block";

import { useEffect } from "react";
import classNames from "classnames";
import { Card, CardSectionProps } from "@/components/ui";
import styles from "./PlaylistsView.module.scss";

export interface PlaylistsViewProps extends CardProps {
  /** The playlists that can be selected */
  playlists: Playlist[];

  /** The playlist */
  playlist?: MutableRefObject<string>;

  /** Callback called when a playlist is selected */
  onSelect?: () => void;

  /** The instruction message */
  instruction?: string;

  /** Title of the card */
  title?: string;

  /** Whether to animate the playlists on render. */
  animate?: boolean;

  /** Animation delay in ms */
  animationDelayMs?: number;
}

/**
 * Playlist is a block view, that handles (auto)selection of a playlist
 */
export default function PlaylistsView({
  playlists,
  playlist: currentPlaylist,
  onSelect = () => {},
  instruction,
  title,
  animate = true,
  animationDelayMs = 100,
  ...cardProps
}: PlaylistsViewProps) {
  // Silently proceed to next view when fewer than 2 playlists are left
  useEffect(() => {
    if (playlists.length < 2) onSelect();
  }, [playlists, onSelect]);

  // Render nothing when there's one or fewer playlists
  if (playlists.length <= 1) return null;

  return (
    <Card {...cardProps}>
      <Card.Header title={title}>{instruction}</Card.Header>
      {playlists.map((playlist, index) => (
        <PlaylistItem
          key={playlist.id}
          playlist={playlist}
          onSelect={(playlistId) => {
            currentPlaylist.current = playlistId;
            onSelect();
          }}
          className={animate && "anim anim-fade-in-slide-left anim-speed-300"}
          style={{ animationDelay: `${index * animationDelayMs}ms` }}
        />
      ))}
    </Card>
  );
}
PlaylistsView.viewName = "playlists";
PlaylistsView.usesOwnLayout = false;
PlaylistsView.getViewProps = ({ playlist, block, onNext, action }) => ({
  playlist,
  playlists: block?.playlists,
  onSelect: onNext,
  instruction: action.instruction,
  title: "Playlists...",
});
PlaylistsView.dependencies = ["playlist", "block", "onNext", "action"];

interface PlaylistItemProps extends CardSectionProps {
  playlist: Playlist;

  /** Callback called when selecting an item. */
  onSelect?: (playlistId: Playlist["id"]) => void;
}

function PlaylistItem({
  playlist,
  onSelect = () => {},
  spacing = "narrow",
  className,
  ...cardSectionProps
}: PlaylistItemProps) {
  return (
    <Card.Option
      data-testid="playlist-item"
      className={classNames(styles.playlistSection, className)}
      onClick={() => onSelect(playlist.id)}
      onKeyPress={() => onSelect(playlist.id)}
      tabIndex={0}
      spacing={spacing}
      {...cardSectionProps}
    >
      <div className={styles.playlistItem}>
        <span className={classNames(styles.icon, "fill-primary")}>
          <i />
        </span>
        <span className={styles.label}>{playlist.name}</span>
      </div>
    </Card.Option>
  );
}
