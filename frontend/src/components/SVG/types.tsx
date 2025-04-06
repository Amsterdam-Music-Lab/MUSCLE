/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

// TODO move these type definitions elsewhere?

export type SVGSolidFill = string;

export type SVGGradientFill = {
  /** 
   * The start color of the gradient. 
   * If not specified, SVGGradient will use the variable --start-color 
   */
  startColor?: string;

  /** 
   * The end color of the gradient 
   * If not specified, SVGGradient will use the variable --end-color
   */
  endColor?: string;
  
  /** The angle of the gradient in degrees */
  angle?: number;

  /** 
   * Scale the endpoints of the gradient. 
   * When scale > 1, the endpoints are placed outside the object. 
   * For scale < 1, they are compressed towards the center.
   */
  scale?: number;
}

/** An SVG fill */
export type SVGFill = SVGSolidFill | SVGGradientFill;
