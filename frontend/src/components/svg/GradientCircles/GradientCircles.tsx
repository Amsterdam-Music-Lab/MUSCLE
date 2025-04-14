/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react";
import classNames from "classnames";
import GradientCirclesSVG, {
  BasicGradientCirclesProps,
} from "./GradientCirclesSVG";
import styles from "./GradientCircles.module.scss";

interface GradientCirclesProps
  extends React.HTMLAttributes<HTMLDivElement>,
    BasicGradientCirclesProps {
  /** The size of the blur in pixels */
  blur?: number;
}

/**
 * A div filled with randomly positioned gradient circles, and
 * an optional blur over it. The circles can also be animated, in
 * which case the gradient will slowly rotate. The colors, number
 * of circles, and the blur can all be set. See GradientCirclesSVG
 * for more details.
 */
export default function GradientCircles({
  fill,
  blur = 0,
  animate = false,
  numCircles,
  minRadiusFactor,
  meanDuration,
  aspect,
  height,
  ...props
}: GradientCirclesProps) {
  const { style, className, ...rest } = props;
  return (
    <div
      className={classNames(styles.gradientCircles, className)}
      style={{ "--blur": `${blur}px`, ...style }}
      {...rest}
    >
      <div className={styles.innerWrapper}>
        <GradientCirclesSVG
          fill={fill}
          aspect={aspect}
          height={height}
          animate={animate}
          numCircles={numCircles}
          meanDuration={meanDuration}
          minRadiusFactor={minRadiusFactor}
        />
      </div>
      {blur !== 0 && (
        <div className={styles.blur}>
          <div />
        </div>
      )}
    </div>
  );
}
