/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { Fill, SVGSymbolName, SVGSymbolProps } from "./svg";
import { Variant } from "./themeProvider";

export interface TimelineStep extends SVGSymbolProps {
  symbol?: SVGSymbolName;
  trophy: boolean;
}

export interface BaseTimeline {
  /** The current active step */
  currentStep?: number;

  dotSize?: number;

  trophySize?: number;

  showDots?: boolean;

  /** Theme variant. If set, this should override the fill. */
  variant?: Variant;

  /** Fill: an SVG fill object specifying either a fill or a color */
  fill?: Fill;

  /** Whether to animate the symbol, e.g. by rotating it or the gradient. */
  animate?: boolean;
}

interface TimelineBySteps extends BaseTimeline {
  steps: TimelineStep[];
}

interface TimelineBySymbols extends BaseTimeline {
  symbols: SVGSymbolName[];
}

/**
 * A timeline object specifies the symbols at all timesteps.
 *
 * This can be done in two ways. Option 1 is to specify all steps:
 *
 *  {
 *    steps: [
 *      { symbol: "dot", size: 10, ... },
 *      { symbol: "star-4", size:20, ... },
 *      ...
 *    ],
 *    variant: "primary", // defaults passed to each of the steps
 *    ...
 *  }
 *
 * Option 2 is to specify only the symbol names:
 *
 *  {
 *    symbols: ['dot', 'dot', 'star-4', 'dot', ...],
 *    size: 20,
 *    dotSize: 10,
 *    ...
 *  }
 *
 */
export type TimelineConfig = TimelineBySteps | TimelineBySymbols;

// export type TimelineConfig = TimelineStep[];
