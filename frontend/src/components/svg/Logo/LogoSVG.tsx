/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { SVGAttributes } from "react";
import type { LogoBaseProps } from "./Logo";
import { Gradient } from "../Gradient";

interface LogoSVGProps
  extends LogoBaseProps,
    Omit<SVGAttributes<SVGSVGElement>, "fill" | "type"> {
  width: number;
  height: number;
}

export default function LogoSVG({
  fill,
  width,
  height,
  children,
  ...svgProps
}: LogoSVGProps) {
  const id = `${Math.random().toString(16).slice(2)}`;
  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...svgProps}
    >
      <rect width={width} height={height} />
      <g fill={typeof fill === "object" ? `url(#gradient-${id})` : fill}>
        {children}
      </g>
      <defs>
        {typeof fill === "object" && (
          <Gradient
            id={`gradient-${id}`}
            {...fill}
            scale={2 * Math.max(width, height)}
            gradientUnits="userSpaceOnUse"
          />
        )}
      </defs>
    </svg>
  );
}
