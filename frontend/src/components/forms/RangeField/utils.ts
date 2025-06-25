/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { RangeOption } from "./RangeField";

export function generateOptions<Value>(
  min: number,
  max: number,
  step: number,
  autoTickLabels: boolean
): RangeOption<Value>[] {
  const options = [];
  for (let val = min; val <= max; val += step) {
    options.push({
      value: val,
      label: autoTickLabels ? String(val) : undefined,
      position: val,
    });
  }
  return options;
}

export function havePositions<Value>(options: RangeOption<Value>[]) {
  return options.map((opt) => opt?.position).every(Boolean);
}

export function getTickLabels<Value>(
  options: RangeOption<Value>[],
  showIntermediateTickLabels: boolean
) {
  return options.map((option, index) => {
    if (!showIntermediateTickLabels) {
      return index === 0 || index === options.length - 1
        ? option.label
        : undefined;
    }
    return option?.label;
  });
}

export function processRangeFieldConfig(
  options,
  min,
  max,
  step,
  tickLabels,
  autoTickLabels,
  showIntermediateTickLabels
) {
  // Ensure we have both a valid options object and min, max and step defined.
  if (
    (!options || !options?.length) &&
    (min === undefined || max === undefined || step === undefined)
  ) {
    throw Error("Either provide `options` or `min`, `max` and `step`");
  }
  if (options) {
    // Add positions if the options don't have positions yet
    if (!havePositions(options))
      options.forEach((opt, idx) => (opt.position = idx));

    // Infer the min and max position, and the stepsize
    min = options[0].position!;
    max = options[options.length - 1].position!;
    step = step ?? (max - min) / (options.length - 1);
  } else {
    options = generateOptions(min!, max!, step!, autoTickLabels);
  }

  // Use tickLabels if specified, otherwise get the labels from option.label.
  if (tickLabels && tickLabels.length !== options.length) {
    console.warn("`tickLabels` should have the same length as `option`");
  }
  tickLabels = tickLabels ?? getTickLabels(options, showIntermediateTickLabels);

  return { options, min, max, step, tickLabels };
}
