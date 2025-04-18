/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { SVGProps } from "react";
import type { Fill } from "@/types/svg";
import type { Variant } from "@/types/themeProvider";
import { Gradient } from "../Gradient";
import { useVariantFill } from "@/hooks/useVariantFill";

interface BasicDotProps {
  /** Size of the dot */
  size?: number;

  /** Fill object or string */
  fill?: Fill;

  /** Whether to animate the object */
  animate?: boolean;

  /** Theme variant. If set, this overrides the fill. */
  variant?: Variant;
}

interface DotProps
  extends Omit<
      SVGProps<SVGSVGElement>,
      "width" | "height" | "viewBox" | "fill"
    >,
    BasicDotProps {}

/**
 * A simple SVG dot with a given size and fill. The dot can be animated.
 */
export default function Dot({
  size = 20,
  fill,
  animate = false,
  variant,
  ...props
}: DotProps) {
  const id = `${Math.random().toString(16).slice(2)}`;
  const variantFill = useVariantFill(variant ?? "primary") ?? "#000";
  fill = fill ?? variantFill;

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} {...props}>
      <defs>
        {typeof fill === "object" && (
          <Gradient id={`gradient-${id}`} {...fill} />
        )}
      </defs>
      <circle
        cx={size / 2}
        cy={size / 2}
        r={(size - 1) / 2}
        fill={typeof fill === "object" ? `url(#gradient-${id})` : fill}
        className={animate ? "animate-rotate" : ""}
      />
    </svg>
  );
}
