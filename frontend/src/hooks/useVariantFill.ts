/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { useTheme } from "@/theme/ThemeProvider";
import { type Variant } from "@/theme/themes";
import { type GradientFill } from "@/components/svg/types";

/**
 * Hook that returns the fill for a given variant,
 * using the fills specified in the theme.
 */
export function useVariantFill(variant: Variant): GradientFill | undefined {
  const theme = useTheme();
  if (!theme.theme || !theme.theme[variant]) {
    return undefined;
  }
  const _variant = theme?.theme[variant];
  const fill = {
    endColor: _variant.endColor,
    startColor: _variant.startColor,
    angle: _variant?.angle,
    scale: _variant?.scale,
  };
  return fill;
}
