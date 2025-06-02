/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { BaseButtonProps, ButtonProps } from "@/components/ui";
import { forwardRef } from "react";
import classNames from "classnames";
import { Button } from "@/components/ui";

export interface BasePlayButtonProps extends BaseButtonProps {
  /** Play handle */
  onClick?: (section: number) => void;

  /** Whether the button is playing */
  playing: boolean;

  /**
   * If true, the button will be disabled whenever playing is true.
   */
  disableWhenPlaying?: boolean;
}

export interface PlayButtonProps
  extends BaseButtonProps,
    Omit<ButtonProps, "onClick"> {}

/**
 * A huge play button that shows a play or stop icon depending on whether
 * playing is true.
 */
const PlayButton = forwardRef(function PlayButton(
  {
    onClick,
    playing,
    disableWhenPlaying = true,
    disabled,
    size = "huge",
    ...buttonProps
  }: PlayButtonProps,
  ref
) {
  disabled = disableWhenPlaying && playing ? true : disabled;
  const handlePlay = () => {
    if (onClick && !disabled) onClick(0);
  };
  return (
    <Button
      ref={ref}
      role="button"
      tabIndex={0}
      onClick={handlePlay}
      onKeyDown={handlePlay}
      disabled={disabled}
      size={size}
      data-state={playing ? "playing" : "stopped"}
      {...buttonProps}
    >
      <i className={classNames("fa", playing ? "fa-stop" : "fa-play")} />
    </Button>
  );
});

PlayButton.displayName = "PlayButton";
export default PlayButton;
