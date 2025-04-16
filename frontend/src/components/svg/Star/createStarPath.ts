/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

/**
 * Helper to round the coordinates
 */
const round = (n: number) => Math.round(n * 1e6) / 1e6;

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
export default function createStarPath({
  cx,
  cy,
  numPoints,
  innerRadius,
  outerRadius,
}: CreateStarPathProps): string {
  let path = "";
  const angle = (Math.PI * 2) / numPoints; // Angle between points

  for (let i = 0; i < numPoints * 2; i++) {
    const r = i % 2 === 0 ? outerRadius : innerRadius;
    const x = round(cx + r * Math.cos((i * angle) / 2));
    const y = round(cy + r * Math.sin((i * angle) / 2));
    path += i === 0 ? `M ${x},${y}` : ` L ${x},${y}`;
  }

  return path + " Z"; // Close the path
}
