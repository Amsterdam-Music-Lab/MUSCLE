/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react";
import { gradientId, SVGGradient } from "@/components/SVG/SVGGradient";
import { SVGCircle } from "@/components/SVG/SVGCircle";


export interface BasicGradientCirclesProps {
  /** Starting color of the linear gradient */
  color1: string;

  /** End color of the linear gradient */
  color2: string;

  /** The aspect ratio of the SVG */
  aspect?: number;

  /** Height of the SVG */
  height?: number;

  /** The number of circles in the SVG */
  numCircles?: number;

  /** 
   * Offset for the endpoints of the gradients. 
   * When >0 the endpoints are moved outside of the gradient. 
   */
  gradientOffset?: number;
  
  /** Whether to rotate the gradients */
  animate?: boolean

  /** 
   * The mean duration of the animation (when animate=true). 
   * Note that the actual duration is computed as  meanDuration + Math.random() * meanDuration 
   */
  meanDuration?: number;

  /** 
   * The minimum radius as a fraction of the SVGs width. 
   * A radius is then sampled using minRadius + 10^(1 + 3 * rand) 
   * where rand is a random float between 0 and 1. 
   */
  minRadiusFactor?: number;
}


interface GradientCirclesSVGProps extends React.SVGAttributes<SVGSVGElement>, BasicGradientCirclesProps {}


/**
 * An SVG filled with randomly positioned gradient circles, which
 * can also be animated by rotating the gradient. The colors, number 
 * of circles, and the blur can all be set. Note that the duration of 
 * the animation is random, but you can  set the mean duration. The 
 * radius of the circles is also randomly determined using 
 *    minRadius + 10^(1 + 3 * rand) 
 * where rand is a random float between 0 and 1.
 */
export default function GradientCirclesSVG({
  color1 = "#ff0000",
  color2 = "#0000ff",
  aspect = 1,
  height = 2000,
  numCircles = 12,
  gradientOffset = 0.35,
  animate = true,
  meanDuration = 5,
  minRadiusFactor = 0.2,
  ...props
}: GradientCirclesSVGProps) {
  
  const width = height * aspect;
  const minRadius = minRadiusFactor * width;
  const id = gradientId()
  const circleData = Array.from({ length: numCircles })
    .map(() => ({
      cx: Math.random() * width,
      cy: Math.random() * height,
      r: minRadius + Math.pow(10, 1 + 3 * Math.random()),
      rotate: Math.random() * 360,
      dur: meanDuration + Math.random() * meanDuration,
      fill: `url(#${id})`,
      animate: animate
    }))
    .sort((a, b) => (a.r - b.r) * Math.random() < 0);

  // Pass all other options to the outer svg element
  const { viewBox: _viewBox, xmlns: _xmlns, ...rest } = props;

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      xmlns="http://www.w3.org/2000/svg"
      {...rest}
    >
      <g clipPath="url(#clip-path)">
        <rect
          width={width}
          height={height}
          fill={`url(#${id})`}
        />
        {circleData.map((circle, i) => (
          <SVGCircle key={i} {...circle} />
        ))}
      </g>

      <defs>
        <SVGGradient 
          id={id}
          from={color1} 
          to={color2} 
          x1={-1 * gradientOffset} 
          y1={0} 
          x2={1 + gradientOffset} 
          y2={0} />
        <clipPath id="clip-path">
          <rect width={width} height={height} fill={`url(#${id})`} />
        </clipPath>
      </defs>
    </svg>
  );
}
