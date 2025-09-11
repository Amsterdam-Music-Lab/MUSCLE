/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { Children, isValidElement } from "react";
import type { CSSProperties, HTMLAttributes } from "react";
import classNames from "classnames";
import {
  OrientationProvider,
  useOrientation,
} from "@/hooks/OrientationProvider";
import styles from "./SquareLayout.module.scss";

interface SectionProps extends HTMLAttributes<HTMLDivElement> {}

export interface SquareLayoutProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * Height of the square in landscape orientation, given as a fraction (!)
   * of the available height. So .8 indicates it should be 80% of the available
   * height.
   */
  landscapeSquareHeight?: number;

  /** Aspect ratio of the container in landscape orientation */
  landscapeAspectRatio?: number;

  /**
   * Height of the header in portrait mode as a fraction of available space
   * left above/below the square. This is used to set the flex_basis property
   * of the header; the footer and aside will take up the rest of the space.
   * If portraitHeaderHeight is 1, the header is as large as possible, if it is
   * 0 it is as small as possible.
   */
  portraitHeaderHeight: number;

  /** Aspect ratio of the container in portrait orientation */
  portraitAspectRatio?: number;

  /** Whether to color the sections for debugging purposes */
  debug?: boolean;
}

/**
 * A layout component that divides the view in four areas: a header, square,
 * footer and an aside. In landscape orientation, the header is shown left,
 * the square right, the aside under the header and the footer under the square.
 * In portrait orientation, the header, square, footer and aside are stacked
 * vertically. The square always maintains square aspect ratio; the container
 * as a whole also maintains its aspect ratio, which can be different depending
 * on the orientation. Note that no children other than header, footer, aside
 * and square are accepted. You can create them using SquareLayout.Header, etc.
 */
function SquareLayoutInner({
  children,
  className,
  debug = false,
  landscapeSquareHeight = 0.85,
  landscapeAspectRatio = 13 / 10,
  portraitHeaderHeight = 0.5,
  portraitAspectRatio = 4 / 8,
  ...divProps
}: SquareLayoutProps) {
  const orientation = useOrientation();

  // Filter children, only accept header, square, footer and aside
  const allChildren = Children.toArray(children);
  let header, square, footer, aside;
  for (const child of allChildren) {
    if (!isValidElement(child)) continue;
    switch (child.type) {
      case SquareLayout.Header:
        header = child;
        break;
      case SquareLayout.Square:
        square = child;
        break;
      case SquareLayout.Footer:
        footer = child;
        break;
      case SquareLayout.Aside:
        aside = child;
        break;
      default:
        console.warn("Unknown child passed to SquareLayout", child);
    }
  }
  return (
    <div
      className={classNames(styles.wrapper, debug && styles.debug, className)}
      data-orientation={orientation}
      style={
        {
          "--sl-landscape-square-height": landscapeSquareHeight,
          "--sl-landscape-aspect-ratio": landscapeAspectRatio,
          "--sl-landscape-aspect-ratio-inverse": 1 / landscapeAspectRatio,
          "--sl-portrait-header-height": portraitHeaderHeight,
          "--sl-portrait-aspect-ratio": portraitAspectRatio,
        } as CSSProperties
      }
      {...divProps}
    >
      <div className={styles.padding}>
        <div className={styles.container}>
          {header}
          {square}
          {footer}
          {aside}
        </div>
      </div>
    </div>
  );
}

function SquareLayout({
  fullscreen,
  children,
  ...props
}: SquareLayoutProps & { fullscreen: boolean }) {
  return (
    <OrientationProvider fullscreen={true}>
      <SquareLayoutInner {...props}>{children}</SquareLayoutInner>
    </OrientationProvider>
  );
}

// Sections

SquareLayout.Header = ({ className, ...props }: SectionProps) => (
  <div
    className={classNames(styles.header, styles.sideCol, className)}
    {...props}
  />
);

SquareLayout.Square = ({ className, children, ...props }: SectionProps) => (
  <div
    className={classNames(styles.square, styles.mainCol, className)}
    {...props}
  >
    {children}
  </div>
);

SquareLayout.Aside = ({ className, ...props }: SectionProps) => (
  <div className={classNames(styles.aside, className)} {...props} />
);

SquareLayout.Footer = ({ className, ...props }: SectionProps) => (
  <div className={classNames(styles.footer, className)} {...props} />
);

export default SquareLayout;
