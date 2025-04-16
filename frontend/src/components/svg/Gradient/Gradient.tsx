/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { GradientFill } from "@/types/svg";

interface GradientProps
  extends GradientFill,
    Omit<JSX.IntrinsicElements["linearGradient"], "x1" | "y1" | "x2" | "y2"> {}

/**
 * An SVG gradient defined by two colors, an angle and a scale.
 */
export default function Gradient({
  id,
  startColor,
  endColor,
  angle = 0,
  scale = 1,
  gradientUnits = "objectBoundingBox",
  ...props
}: GradientProps) {
  const angleRad = angle * (Math.PI / 180);
  const cx = 0.5;
  const cy = 0.5;
  const dx = Math.cos(angleRad) * scale * cx;
  const dy = Math.sin(angleRad) * scale * cy;
  const x1 = cx - dx;
  const y1 = cy - dy;
  const x2 = cx + dx;
  const y2 = cy + dy;

  return (
    <linearGradient
      id={id}
      x1={x1}
      y1={y1}
      x2={x2}
      y2={y2}
      gradientUnits={gradientUnits}
      {...props}
    >
      <stop stopColor={startColor || "var(--start-color)"} />
      <stop offset="1" stopColor={endColor || "var(--end-color)"} />
    </linearGradient>
  );
}
