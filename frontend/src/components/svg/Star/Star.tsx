/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react"
import { Gradient } from "../Gradient";
import { type Fill } from "../types";

interface CreateStarPathProps {
  /** The x-coordinate of the center */
  cx: number;

  /** The y-coordinate of the center */
  cy: number;

  /** Number of points of the star */
  numPoints: number;

  /** Inner radius of the star */
  innerRadius: number;

  /** The outer radius of the star */
  outerRadius: number;
}

/**
 * Return the path string of an star with a given number of points and a 
 * given inner- and outer radius.
 */
function createStarPath({
  cx, cy, numPoints, innerRadius, outerRadius
}: CreateStarPathProps): string {
  let path = "";
  const angle = (Math.PI * 2) / numPoints; // Angle between points

  for (let i = 0; i < numPoints * 2; i++) {
    const r = i % 2 === 0 ? outerRadius : innerRadius;
    const x = cx + r * Math.cos(i * angle / 2);
    const y = cy + r * Math.sin(i * angle / 2);
    path += i === 0 ? `M ${x},${y}` : ` L ${x},${y}`;
  }

  return path + " Z"; // Close the path
};


interface BasicSVGStarProps {

  /** Number of points of the star */
  numPoints?: number;

  /** 
   * The sharpness of the star, a value between 0 and 1.
   * For sharpness=0, the star becomes a polygon (no points), and 
   * for sharpenss=1, the points are infinitely sharp, so invisible.
   */
  sharpness?: number;

  /** Size of the star */
  size?: number;

  /** Fill: an SVG fill object specifying either a fill or a col */
  fill?: Fill;

  /** Fill of the star when showCircle=true. Defaults to white. */
  starFill?: Fill;

  /** 
   * Whether to show a circle around the star. 
   * When showCircle is false, starFill is ignored, and the star is filled with either
   * the fill color (if provided) or the gradient. StrokeWidthFactor is then also ignored.
   */
  showCircle?: boolean;
  
  /** 
   * Whether to animate the star by rotating it. Note that this
   * only adds an 'animate-rotate' class, so the animation should be set in CSS.
   */
  animate?: boolean;

  /** The width of the circle's stroke as a fraction of the stars' size */
  circleStrokeWidth?: number;

  /** Color of the circle stroke. Defaults to a very transparent white. */
  circleStroke?: string;

  /** 
   * The maximum size of the star, relative to the size of the circle. 
   * When maxRadiusFactor=1, the star is exactly as big as the circle. If 
   * showCircle is false, then maxRadiusFactor is also set to 1. 
   * When maxRadiusFactor=0, the star is infinitely small.
   */
  starSize?: number;
}


/** 
 * All SVG properties are allowed, except width, height and viewBox 
 */
interface SVGStarProps 
  extends 
    BasicSVGStarProps, 
    Omit<React.SVGProps<SVGSVGElement>, 'width' | 'height' | 'viewBox'> 
  {};


/**
 * An SVG star in an optional circle. The number of points and the sharpness of the
 * star can be varied. When the circle is shown, it is by default filled with a gradient,
 * with the star shown in white, and with a very light white border around the circle.
 * All this can be customized.
 */
export default function SVGStar({
  numPoints = 5,
  size = 20,
  fill,
  starFill = "#ffffff",
  animate = true,
  showCircle = true,
  starSize = .7,
  sharpness = .6,
  circleStrokeWidth = 0.2,
  circleStroke = "#ffffff33",
  ...props
}: SVGStarProps) {
  // A unique id to reference svg elements
  const id = `${Math.random().toString(16).slice(2)}`

  // If no circle is shown, use maximum star size.
  if(!showCircle) {
    starSize = 1;
  }

  const center = size / 2; // Center the star
  const strokeWidth = circleStrokeWidth * size;
  const outerRadius = (size * starSize) / 2;
  const innerRadius = (1 - sharpness) * outerRadius; // Scale inner radius
  const pathData = createStarPath({
    cx: center, 
    cy: center, 
    numPoints, 
    innerRadius, 
    outerRadius
  });

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      {...props}
    >
      <defs>
        { showCircle && (
          <>
            {/* We mask the circle by itself to get an 'inner stroke' */}
            <circle
              id={`circle-${id}`}
              cx={size / 2} cy={size / 2} r={(size - 1) / 2}
            />
            <mask id={`mask-${id}`}>
              <rect x="0" y="0" width={size} height={size} fill="black" />
              <use href={`#circle-${id}`} fill="white"/>
            </mask>
          </>
        )}
        { typeof(fill) === "object" && <Gradient id={`circle-gradient-${id}`} {...fill} />}
        { typeof(starFill) === "object" && <Gradient id={`star-gradient-${id}`} {...starFill} />}
      </defs>

      <g className={animate ? "animate-rotate" : ""}>
        <use 
          href={`#circle-${id}`} 
          mask={showCircle ? `url(#mask-${id})` : undefined} 
          fill={typeof(fill) === "object" ? `url(#circle-gradient-${id})` : fill}
          strokeWidth={strokeWidth}
          stroke={circleStroke}
          />
        <path 
          d={pathData} 
          fill={typeof(starFill) === "object" ? `url(#star-gradient-${id})` : starFill} />
      </g>
    </svg>
  );
};