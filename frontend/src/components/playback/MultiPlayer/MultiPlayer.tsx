/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes, ReactNode } from "react";
import type { PlaybackArgs } from "@/types/Playback";
import { SmallPlayer } from "../SmallPlayer";
import classNames from "classnames";
import styles from "./MultiPlayer.module.scss";

export interface MultiPlayerProps extends HTMLAttributes<HTMLDivElement> {
  playSection: (index: number) => void;

  /**
   * The number of sections. Note that this components does not actually
   * require the actual sections.
   */
  numSections: number;

  /**
   * Index of the current (?) player
   */
  playerIndex: string;

  /**
   * Labels for each of the sections
   */
  labels?: PlaybackArgs["labels"];

  /**
   * Indices of disabled players
   */
  disabledPlayers?: number[];

  /**
   * A function returning extra content for every section
   */
  extraContent?: (index: number) => ReactNode;

  /** Whether to center the content in the SmallPlayers */
  center?: boolean;
}

export default function MultiPlayer({
  playSection,
  numSections,
  playerIndex,
  labels,
  disabledPlayers,
  extraContent = () => {},
  center = false,
  className,
  ...divProps
}: MultiPlayerProps) {
  const hasDisabledPlayers = Array.isArray(disabledPlayers);
  const indices = [...Array(numSections).keys()];
  return (
    <div
      className={classNames(styles.multiplayer, className)}
      data-testid="multiplayer"
      {...divProps}
    >
      {indices.map((index) => (
        <SmallPlayer
          key={index}
          center={center}
          onClick={() => playSection(index)}
          rounded={false}
          disabled={hasDisabledPlayers && disabledPlayers.includes(index)}
          playing={parseInt(playerIndex) === index}
          label={labels ? labels[index] : undefined}
        >
          {extraContent(index)}
        </SmallPlayer>
      ))}
    </div>
  );
}
