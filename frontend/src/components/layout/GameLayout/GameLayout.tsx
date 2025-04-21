/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { Children, isValidElement, useEffect, useRef, useState } from "react";
import type { CSSProperties, HTMLAttributes } from "react";
import classNames from "classnames";
import styles from "./GameLayout.module.scss";

export function useContainerOrientation<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  const [orientation, setOrientation] = useState<"portrait" | "landscape">(
    "portrait"
  );

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const threshold = 0.05;

    const observer = new ResizeObserver(([entry]) => {
      const { width, height } = entry.contentRect;
      if (Math.abs(width - height) / Math.max(width, height) < threshold) {
        // Skip updating orientation if too close
        return;
      }

      const newOrientation = width > height ? "landscape" : "portrait";
      setOrientation(newOrientation);
    });

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return { ref, orientation };
}

interface SectionProps extends HTMLAttributes<HTMLDivElement> {}

const GameLayoutHeader = ({ className, ...props }: SectionProps) => (
  <div
    className={classNames(styles.header, styles.sideCol, className)}
    {...props}
  />
);

const GameLayoutMain = ({ className, children, ...props }: SectionProps) => (
  <div
    className={classNames(styles.main, styles.mainCol, className)}
    {...props}
  >
    <div className={styles.square}>{children}</div>
  </div>
);

const GameLayoutFooterLeft = ({ className, ...props }: SectionProps) => (
  <div className={classNames(styles.footerLeft, className)} {...props} />
);

const GameLayoutFooterMain = ({ className, ...props }: SectionProps) => (
  <div
    className={classNames(styles.footerMain, styles.mainCol, className)}
    {...props}
  />
);

export interface GameLayoutProps extends HTMLAttributes<HTMLDivElement> {
  /**  */
  debug?: boolean;
  minAspectLandscape?: number;
  minAspectPortrait?: number;
}
/**
 * A Component
 */
function GameLayout({
  children,
  className,
  debug = false,
  minAspectLandscape = 4 / 3,
  minAspectPortrait = 5 / 3,
  ...divProps
}: GameLayoutProps) {
  const { ref, orientation } = useContainerOrientation<HTMLDivElement>();
  let header = <GameLayout.Header />;
  let main = <GameLayout.Main />;
  let footerLeft = <GameLayout.FooterLeft />;
  let footerMain = <GameLayout.FooterMain />;

  // Filter children
  const allChildren = Children.toArray(children);

  for (const child of allChildren) {
    if (!isValidElement(child)) continue;
    console.log(child);
    switch (child.type) {
      case GameLayout.Header:
        header = child;
        break;
      case GameLayout.Main:
        main = child;
        break;
      case GameLayout.FooterLeft:
        footerLeft = child;
        break;
      case GameLayout.FooterMain:
        footerMain = child;
        break;
      default:
        console.warn("Unknown child passed to GameLayout", child);
    }
  }
  return (
    <div
      className={classNames(
        styles.wrapper,
        styles.constrainAspectRatio,
        debug && styles.debug,
        className
      )}
      data-orientation={orientation}
      style={
        {
          "--min-aspect-landscape": minAspectLandscape,
          "--min-aspect-portrait": minAspectPortrait,
        } as CSSProperties
      }
      {...divProps}
    >
      <div className={styles.container}>
        <div ref={ref} className={classNames(styles.mainRow, styles.row)}>
          {header}
          {main}
        </div>
        <div className={classNames(styles.footer, styles.row)}>
          {footerLeft}
          {footerMain}
        </div>
      </div>
    </div>
  );
}

// Assign statics
GameLayout.Header = GameLayoutHeader;
GameLayout.Main = GameLayoutMain;
GameLayout.FooterLeft = GameLayoutFooterLeft;
GameLayout.FooterMain = GameLayoutFooterMain;

export default GameLayout;
