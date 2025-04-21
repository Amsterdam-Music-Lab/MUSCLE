/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { CSSProperties, HTMLAttributes } from "react";
import classNames from "classnames";
import styles from "./NarrowLayout.module.scss";

export interface NarrowLayoutProps extends HTMLAttributes<HTMLDivElement> {
  /** The maximum width of the layout */
  maxWidth?: number;

  /** Whether the children can run to the horizontal margins (i.e., no padding) */
  flush?: boolean;
}

/**
 * A Component
 */
export default function NarrowLayout({
  className,
  maxWidth = 500,
  flush = true,
  children,
  ...divProps
}: NarrowLayoutProps) {
  return (
    <div
      className={classNames(
        styles.narrowLayout,
        flush && styles.flush,
        className
      )}
      {...divProps}
      style={{ "--narrow-layout-max-width": `${maxWidth}px` } as CSSProperties}
    >
      {children}
    </div>
  );
}
