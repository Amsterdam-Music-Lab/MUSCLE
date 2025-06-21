/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { RangeFieldProps } from "./RangeField";
import RangeField from "./RangeField";

export interface SliderFieldProps<Value>
  extends Omit<RangeFieldProps<Value>, "values" | "onChange"> {
  value?: Value;
  onChange: (newValue: Value) => void;
}

export default function SliderField<Value>({
  value,
  onChange,
  ...props
}: SliderFieldProps<Value>) {
  return (
    <RangeField
      values={value ? [value] : []}
      onChange={(values) => onChange(values[0] ?? undefined)}
      {...props}
    />
  );
}
