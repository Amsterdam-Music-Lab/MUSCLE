/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { symbols } from "@/components/svg/symbols";
import { Variant } from "./themeProvider";

// TODO move these type definitions elsewhere?

export type SolidFill = string;

export type GradientFill = {
  /**
   * The start color of the gradient.
   * If not specified, Gradient will use the variable --start-color
   */
  startColor?: string;

  /**
   * The end color of the gradient
   * If not specified, Gradient will use the variable --end-color
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
};

/** An SVG fill */
export type Fill = SolidFill | GradientFill;

/** Names of SVG symbols (e.g. star-5, dot, ...) */
export type SVGSymbolName = keyof typeof symbols;

/** Properties of an SVG symbol */
export type SVGSymbolProps = {
  /** Size of the star */
  size?: number;

  /** Theme variant. If set, this should override the fill. */
  variant?: Variant;

  /** Fill: an SVG fill object specifying either a fill or a color */
  fill?: Fill;

  /** Whether to animate the symbol, e.g. by rotating it or the gradient. */
  animate?: boolean;
};
