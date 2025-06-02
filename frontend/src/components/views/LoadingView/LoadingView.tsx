/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import classNames from "classnames";
import { Circle } from "@/components/ui";

export interface LoadingViewProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * Label shown inside the circle. Defaults to "Loading..."
   */
  label?: string;

  /**
   * Size of the rotating gap, from 0 = no gap to 1 = only gap.
   * Default 0.02.
   */
  gapSize?: number;

  duration?: number;
  rotate?: boolean;
  running?: boolean;
}

/**
 * Loading is a block view that shows a loading screen
 * It is normally set by code during loading of data
 */
export default function LoadingView({
  label = "Loading...",
  gapSize = 0.02,
  duration = 2,
  rotate = true,
  running = false,
  className,
  ...divProps
}: LoadingViewProps) {
  return (
    <div className={classNames("transition-appear", className)} {...divProps}>
      <Circle
        data-testid="loading"
        duration={duration}
        startTime={gapSize * duration}
        running={running}
        rotate={rotate}
        style={{ margin: "auto" }}
      >
        {label && <span>{label}</span>}
      </Circle>
    </div>
  );
}

LoadingView.viewName = "loading";
LoadingView.usesOwnLayout = false;
LoadingView.getViewProps = undefined;
