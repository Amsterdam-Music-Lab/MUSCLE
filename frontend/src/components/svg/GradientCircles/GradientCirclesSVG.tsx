/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { SVGAttributes } from "react";
import type { Variant } from "@/theme/themes";
import { Gradient } from "../Gradient";
import { Circle } from "../Circle";
import { useVariantFill } from "@/hooks/useVariantFill";
import { type GradientFill } from "../types";

export interface BasicGradientCirclesProps {
  variant?: Variant;

  /** Starting color of the linear gradient */
  fill?: GradientFill;

  /** The aspect ratio of the SVG */
  aspect?: number;

  /** Height of the SVG */
  height?: number;

  /** The number of circles in the SVG */
  numCircles?: number;

  /** Whether to rotate the gradients */
  animate?: boolean;

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

interface GradientCirclesSVGProps
  extends SVGAttributes<SVGSVGElement>,
    BasicGradientCirclesProps {}

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
  variant,
  fill,
  aspect = 1,
  height = 2000,
  numCircles = 12,
  animate = true,
  meanDuration = 5,
  minRadiusFactor = 0.2,
  ...props
}: GradientCirclesSVGProps) {
  console.log(variant);
  // Default to theme variant
  const variantFill = useVariantFill(variant ?? "primary") ?? {
    startColor: "#ff0000",
    endColor: "#0000ff",
    scale: 1.4,
  };
  fill = fill ?? variantFill;

  const width = height * aspect;
  const minRadius = minRadiusFactor * width;
  const id = `${Math.random().toString(16).slice(2)}`;
  const circleData = Array.from({ length: numCircles })
    .map(() => ({
      cx: Math.random() * width,
      cy: Math.random() * height,
      r: minRadius + Math.pow(10, 1 + 3 * Math.random()),
      rotate: Math.random() * 360,
      dur: meanDuration + Math.random() * meanDuration,
      fill: `url(#gradient-${id})`,
      animate: animate,
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
      <g clipPath={`url(#clip-path-${id})`}>
        <rect width={width} height={height} fill={`url(#gradient-${id})`} />
        {circleData.map((circle, i) => (
          <Circle key={i} {...circle} />
        ))}
      </g>

      <defs>
        <Gradient id={`gradient-${id}`} {...fill} />
        <clipPath id={`clip-path-${id}`}>
          <rect width={width} height={height} fill={`url(#gradient-${id})`} />
        </clipPath>
      </defs>
    </svg>
  );
}
