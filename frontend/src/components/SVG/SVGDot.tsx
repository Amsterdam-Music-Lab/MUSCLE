/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from "react";
import SVGGradient from "./SVGGradient";
import { type SVGFill } from "./types";

interface BasicSVGDotProps {
  /** Size of the dot */
  size?: number;

  /** Fill object or string */
  fill?: SVGFill;

  /** Whether to animate the object */
  animate?: boolean;
}

interface SVGDotProps 
  extends 
    Omit<React.SVGProps<SVGSVGElement>, 'width' | 'height' | 'viewBox'>,
    BasicSVGDotProps 
  {};

/**
 * A simple SVG dot with a given size and fill. The dot can be animated.
 */
export default function SVGDot({
  size = 20,
  fill,
  animate = false,
  ...props
}: SVGDotProps) {
  const id = `${Math.random().toString(16).slice(2)}`
  return (
    <svg 
      width={size} 
      height={size} 
      viewBox={`0 0 ${size} ${size}`} 
      {...props}
    >
      <defs>
        {typeof(fill) === 'object' && <SVGGradient id={`gradient-${id}`} {...fill} />}
      </defs> 
      <circle 
        cx={size / 2} 
        cy={size / 2} 
        r={(size - 1) / 2} 
        fill={typeof(fill) === 'object' ? `url(#gradient-${id})` : fill} 
        className={ animate && "animate-rotate"} 
        />
    </svg>
  );
}