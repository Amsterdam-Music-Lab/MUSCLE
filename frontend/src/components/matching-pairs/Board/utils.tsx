/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { ReactNode, HTMLAttributes } from "react";
import { type SlotProps } from "./Board";

export function getDivs(
  num: number = 16,
  divProps: HTMLAttributes<HTMLDivElement> = {}
) {
  return Array(num)
    .fill(1)
    .map((_, i) => (
      <div key={i} data-testid={`card-${i}`} {...divProps}>
        {i + 1}
      </div>
    ));
}

export function getColoredSlots(
  num: number = 16,
  divProps: HTMLAttributes<HTMLDivElement> = {}
): [ReactNode, SlotProps][] {
  return getDivs(num, divProps).map((child, index) => {
    const hue = (index / num) * 360;
    return [
      child,
      {
        style: {
          ...divProps.style,
          borderWidth: "10px",
          borderstyle: "solid",
          borderColor: `hsl(${hue}, 100%, 50%)`,
        },
        "data-testid": `slot-${index}`,
      },
    ];
  });
}
