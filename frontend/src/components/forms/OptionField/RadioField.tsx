/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import OptionField, { OptionFieldProps } from "./OptionField";

export interface RadioFieldProps<Value>
  extends Omit<OptionFieldProps<Value>, "type" | "value"> {
  value: Value;
  warn?: boolean;
}

export default function RadioField<Value>({
  value,
  onChange,
  warn = true,
  ...props
}: RadioFieldProps<Value>) {
  if (warn && Array.isArray(value))
    console.warn(
      "RadioField received an array as value. Different from CheckboxInput, the value of a RadioField should NOT be an array of values, but just a single value. You can turn this warning off by passing warn={false} to RadioField."
    );
  function handleChange(values: Value[]) {
    return onChange(values[values.length - 1] ?? undefined);
  }
  return (
    <OptionField
      type="radio"
      values={[value]}
      onChange={handleChange}
      {...props}
    />
  );
}
