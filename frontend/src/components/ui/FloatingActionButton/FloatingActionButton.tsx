/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { ButtonHTMLAttributes } from "react";
import type { OverlayProps } from "../Overlay";

import classNames from "classnames";
import { Overlay } from "../Overlay";
import styles from "./FloatingActionButton.module.scss";

type Position =
  | "bottom-left"
  | "bottom-right"
  | "top-left"
  | "top-right"
  | "center-left"
  | "center-right";

export interface FloatingActionButtonProps extends OverlayProps {
  /** Font Awesome icon class name (e.g. 'fa-comment') */
  icon?: string;

  /**
   * The position of the floating action button: 'bottom-left',
   * 'bottom-right', 'top-left', 'top-right', 'center-left',
   * 'center-right' (default)
   */
  position?: Position;
}

export default function FloatingActionButton({
  icon = "fa-comment",
  position = "center-right",
  ...overlayProps
}: FloatingActionButtonProps) {
  const Handle = (props) => (
    <FloatingActionHandle icon={icon} position={position} {...props} />
  );
  return <Overlay Handle={Handle} {...overlayProps} />;
}

interface FloatingActionHandleProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  icon: string;
  position: Position;
}

function FloatingActionHandle({
  position,
  icon,
  ...props
}: FloatingActionHandleProps) {
  return (
    <button
      data-testid="floating-action-button"
      className={classNames(
        styles.button,
        ...position.split("-").map((pos) => styles[pos])
      )}
      {...props}
    >
      <i
        data-testid="floating-action-icon"
        className={classNames(styles.icon, "fa", icon)}
      />
    </button>
  );
}
