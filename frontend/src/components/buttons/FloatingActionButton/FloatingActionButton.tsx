/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { ButtonHTMLAttributes } from "react";
import type { Variant } from "@/types/themeProvider";
import type { OverlayProps } from "@/components/ui";

import classNames from "classnames";
import { Overlay } from "@/components/ui";
import styles from "./FloatingActionButton.module.scss";

type Position =
  | "bottom-left"
  | "bottom-right"
  | "top-left"
  | "top-right"
  | "center-left"
  | "center-right";

interface FloatingActionHandleBaseProps {
  /** Font Awesome icon class name. Default 'fa-comment' */
  icon?: string;

  /**
   * The position of the floating action button: 'bottom-left',
   * 'bottom-right', 'top-left', 'top-right', 'center-left',
   * 'center-right'. Default value 'bottom-right'.
   */
  position?: Position;

  /**
   * Whether to align the handle flush to the edge of the window.
   * Default false.
   */
  flush?: boolean;

  /** The variant to use of the handle; default 'primary'. */
  variant?: Variant;

  /**
   * The offset from the window edge in rems. Default 1.
   */
  offset?: number;

  /**
   * The font size in rems. Default 1.25
   */
  fontSize?: number;
}

export interface FloatingActionButtonProps
  extends OverlayProps,
    FloatingActionHandleBaseProps {}

/**
 * Shows a floating button that opens an overlaid dialog when clicked.
 */
export default function FloatingActionButton({
  icon,
  position,
  flush,
  variant,
  offset,
  fontSize,
  ...overlayProps
}: FloatingActionButtonProps) {
  const Handle = (props) => (
    <FloatingActionHandle
      icon={icon}
      position={position}
      flush={flush}
      variant={variant}
      offset={offset}
      fontSize={fontSize}
      {...props}
    />
  );
  return <Overlay Handle={Handle} {...overlayProps} />;
}

interface FloatingActionHandleProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    FloatingActionHandleBaseProps {}

function FloatingActionHandle({
  position = "bottom-right",
  icon = "fa-comment",
  flush = false,
  variant = "primary",
  offset = 1,
  fontSize = 1.25,
  style,
  className,
  ...props
}: FloatingActionHandleProps) {
  return (
    <button
      data-testid="floating-action-button"
      className={classNames(
        styles.button,
        flush && styles.flushToWindowEdge,
        variant && `fill-${variant}`,
        ...position.split("-").map((pos) => styles[pos]),
        className
      )}
      style={{
        "--fa-button-font-size": `${fontSize}rem`,
        "--fa-button-offset": `${offset}rem`,
      }}
      {...props}
    >
      <i
        data-testid="floating-action-icon"
        className={classNames(styles.icon, "fa", icon)}
      />
    </button>
  );
}
