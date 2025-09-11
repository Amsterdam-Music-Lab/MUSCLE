/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { ButtonHTMLAttributes } from "react";
import type { Variant } from "@/types/themeProvider";
import type { ModalProps } from "@/components/ui";

import classNames from "classnames";
import { Modal } from "@/components/ui";
import styles from "./FloatingActionButton.module.scss";
import { Icon } from "@/components/icons";
import { IconName } from "@/components/icons";

type Position =
  | "bottom-left"
  | "bottom-right"
  | "top-left"
  | "top-right"
  | "center-left"
  | "center-right";

interface FloatingActionHandleBaseProps {
  /** Icon name, default 'comment' */
  iconName?: IconName;

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
  extends ModalProps,
    FloatingActionHandleBaseProps {}

/**
 * Shows a floating button that opens an overlaid dialog when clicked.
 */
export default function FloatingActionButton({
  iconName,
  position,
  flush,
  variant,
  offset,
  fontSize,
  ...modalProps
}: FloatingActionButtonProps) {
  const Handle = (props) => (
    <FloatingActionHandle
      iconName={iconName}
      position={position}
      flush={flush}
      variant={variant}
      offset={offset}
      fontSize={fontSize}
      {...props}
    />
  );
  return <Modal Handle={Handle} {...modalProps} />;
}

interface FloatingActionHandleProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    FloatingActionHandleBaseProps {}

function FloatingActionHandle({
  position = "bottom-right",
  iconName = "comment",
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
      <Icon name={iconName} data-testid="floating-action-icon" />
    </button>
  );
}
