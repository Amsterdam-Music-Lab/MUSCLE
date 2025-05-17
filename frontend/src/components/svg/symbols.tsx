/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { StarProps } from "./Star";

import { Star } from "./Star";
import { Dot } from "./Dot";

export const symbols = {
  dot: Dot,

  star: (props: StarProps) => <Star numPoints={5} {...props} />,

  "star-4": (props: Omit<StarProps, "numPoints">) => (
    <Star numPoints={4} {...props} />
  ),

  "star-5": (props: Omit<StarProps, "numPoints">) => (
    <Star numPoints={5} {...props} />
  ),

  "star-6": (props: Omit<StarProps, "numPoints">) => (
    <Star numPoints={6} {...props} />
  ),

  "star-7": (props: Omit<StarProps, "numPoints">) => (
    <Star numPoints={7} {...props} />
  ),

  "star-8": (props: Omit<StarProps, "numPoints">) => (
    <Star numPoints={8} {...props} />
  ),
};
