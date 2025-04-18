/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { GradientFill } from "@/types/svg";
export type { ThemeName } from "@/theme/themes";

type Color = string;

export type Variant = "primary" | "secondary";

export interface ThemeFill extends GradientFill {
  /** The color to use when useGradients is false  */
  solid: Color;

  /** The gradient scale used for the subtle gradient variant */
  subtleScale: number;

  /** The angle of the gradient */
  angle?: number;

  /** The offset of the gradient (as a percentage) */
  offset?: number;
}

export interface Theme {
  name: string;

  /** Whether the theme is light or dark */
  type: "light" | "dark";

  /** Url of the webfont (typically google fonts) */
  fontUrl?: string;

  /** Font family */
  fontFamily?: string;

  /** Whether to use gradients */
  useGradients: boolean;

  /** Background color */
  background?: Color;

  /** Url to the background image */
  backgroundUrl?: string;

  /** Text color */
  text?: Color;

  /** The primary fill, by default a gradient */
  primary: ThemeFill;

  /** Secondary fill, by default a gradient */
  secondary: ThemeFill;

  /** Default, medium border radius in rem. */
  borderRadius: number;
}
