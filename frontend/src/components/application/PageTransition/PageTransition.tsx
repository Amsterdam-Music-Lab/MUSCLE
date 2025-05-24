/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { CSSProperties, HTMLAttributes } from "react";
import { useRef } from "react";
import { CSSTransition, SwitchTransition } from "react-transition-group";
import styles from "./PageTransition.module.scss";

interface PageTransitionProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * A key that indicates the state of the child element.
   * Change this to trigger a transition.
   */
  transitionKey: any;

  /**
   * The total duration of the transition in ms. Default 500ms.
   */
  durationMs?: number;

  /**
   * The vertical distance in px by which the entering and
   * exiting elements are translated. Note that the exiting
   * element is always moving twice as far. Default 50px.
   */
  distance?: number;

  /**
   * The ratio determines how the transition time is divided
   * between the entering and exiting phase. The default ratio
   * of .75 means that 75% of the time is used for entering
   * and 25% for exititing.
   */
  ratio?: number;
}

/**
 * A wrapper around the SwitchTransition component that shows
 * a smooth page transition.
 */
export default function PageTransition({
  transitionKey,
  durationMs = 500,
  distance = 50,
  ratio = 0.75,
  children,
  style,
  ...divProps
}: PageTransitionProps) {
  const nodeRef = useRef(null);
  return (
    <div
      style={
        {
          "--transition-duration": `${durationMs}ms`,
          "--transition-distance": `${distance}px`,
          "--transition-ratio": ratio,
          ...style,
        } as CSSProperties
      }
      {...divProps}
    >
      <SwitchTransition>
        <CSSTransition
          key={transitionKey}
          nodeRef={nodeRef}
          timeout={{
            exit: (1 - ratio) * durationMs,
            enter: ratio * durationMs,
          }}
          classNames={{
            enter: styles.enter,
            enterActive: styles.enterActive,
            exit: styles.exit,
            exitActive: styles.exitActive,
          }}
          unmountOnExit
        >
          <div ref={nodeRef}>{children}</div>
        </CSSTransition>
      </SwitchTransition>
    </div>
  );
}
