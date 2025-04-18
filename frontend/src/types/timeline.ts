/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

export type TimelineSymbolName =
  | "dot"
  | "star"
  | "star-4"
  | "star-5"
  | "star-6"
  | "star-7"
  | null;

export type TimelineConfig = Array<{
  symbol: TimelineSymbolName;
  size: number;
  animate: boolean;
  trophy: boolean;
}>;
