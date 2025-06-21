/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import OptionField, { OptionFieldProps } from "./OptionField";

export interface CheckboxFieldProps<Value>
  extends Omit<OptionFieldProps<Value>, "type"> {}

/**
 * An input component that shows several checkbox options and allows
 * the user to select one or multiple of these.
 *
 * Note that this component is a very thin wrapper around OptionField.
 */
export default function CheckboxField<Value>({
  value,
  ...props
}: CheckboxFieldProps<Value>) {
  if (!Array.isArray(value))
    console.warn(
      "CheckboxField received a value that is not an array. This may cause unexpected behaviour."
    );
  return <OptionField type="checkbox" values={value} {...props} />;
}
