/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react";
import GradientCirclesSVG, { BasicGradientCirclesProps } from "./GradientCirclesSVG";
import "./GradientCircles.scss";

interface GradientCirclesProps extends React.HTMLAttributes<HTMLDivElement>,BasicGradientCirclesProps {
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
  color1,
  color2,
  blur = 0,
  animate = false,
  gradientOffset,
  numCircles,
  minRadiusFactor,
  meanDuration,
  aspect,
  height,
  ...props
} : GradientCirclesProps) {
  const {style, className, ...rest} = props;
  return (
    <div 
      className={`gradient-circles ${className}`} 
      style={{"--blur": `${blur}px`, ...style}} 
      {...rest}
    >
      <div className="gradient-circles-wrapper">
        <GradientCirclesSVG 
          color1={color1} 
          color2={color2} 
          aspect={aspect}
          height={height}
          animate={animate} 
          gradientOffset={gradientOffset}
          numCircles={numCircles} 
          meanDuration={meanDuration}
          minRadiusFactor={minRadiusFactor}
          />
      </div>
      {blur !== 0 && <div className="gradient-circles-blur"><div /></div>}
    </div>
  );
}