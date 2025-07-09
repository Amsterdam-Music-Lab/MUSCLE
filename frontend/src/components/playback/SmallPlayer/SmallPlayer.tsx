/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import { useRef, useState } from "react";
import { BasePlayButtonProps, PlayButton } from "../PlayButton";
import classNames from "classnames";
import styles from "./SmallPlayer.module.scss";

export interface SmallPlayerProps
  extends BasePlayButtonProps,
    HTMLAttributes<HTMLDivElement> {
  /** Callback called when you click anywhere on the player (not just the button) */
  onClick?: () => void;

  /** Optional label shown below the player */
  label?: string;

  /** Whether to center the content */
  center?: boolean;
}

/**
 * A small player: basically a PlayButton with some text under it.
 */
export default function SmallPlayer({
  label,
  onClick = () => {},
  playing,
  disabled,
  disableWhenPlaying = true,
  size = "lg",
  variant,
  rounded,
  stretch = true,
  outline = true,
  center = true,
  className,
  children,
  ...divProps
}: SmallPlayerProps) {
  const [hovered, setHovered] = useState(false);
  const btnRef = useRef(null);
  disabled = disableWhenPlaying && playing ? true : disabled;
  const handleClick = () => {
    if (!disabled) onClick();
  };
  return (
    <div
      data-testid="player-small"
      role="button"
      onClick={handleClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={classNames(
        styles.smallPlayer,
        center && styles.center,
        "transition-appear",
        disabled && styles.disabled,
        className
      )}
      {...divProps}
    >
      <PlayButton
        ref={btnRef}
        // onClick={onClick}
        playing={playing}
        disabled={disabled}
        size={size}
        variant={variant}
        stretch={stretch}
        outline={outline}
        rounded={rounded}
        hover={hovered}
      />
      {label && (
        <p className={styles.label} data-testid="label">
          {label}
        </p>
      )}
      {children}
    </div>
  );
}
