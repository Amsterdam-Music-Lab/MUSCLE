/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, ReactNode } from "react";
import type { FieldOption, FieldProps } from "../types";
import type { Variant } from "@/types/themeProvider";

import classNames from "classnames";
import { useFieldWrapper } from "../FieldWrapper";
import Option from "./Option";
import styles from "./OptionField.module.scss";
import "@/scss/theme.scss";

export interface OptionFieldProps<Value>
  extends Omit<FieldProps<Value>, "value" | "onChange">,
    Omit<
      HTMLAttributes<HTMLFieldSetElement>,
      "ariaDescribedBy" | "ariaInvalid"
    > {
  /**
   * This does not have to be specified manually: it is set by
   * `CheckboxField` and `RadioField`.
   */
  type: "radio" | "checkbox";

  /** The currently selected options */
  values: Value[];

  /** Callback called when the selection changes */
  onChange: (newValues: Value[]) => void;

  /**
   * A list of possible options to choose from. Each option has properties
   * like `value`, `label`, and `disabled`.
   */
  options: FieldOption<Value>[];

  /** Optional legend shown above the option group. */
  label?: ReactNode;

  /** Theme variant used to fill selected options */
  variant?: Variant;

  tabIndex?: number;
}

/**
 * > ⚠️ **Do not use `OptionField` directly — use `CheckboxField` or `RadioField` instead.**
 *
 * `OptionField` implements a generic option group: a list of options from which
 * one or more values can be selected. It renders standard HTML form elements
 * to ensure native keyboard navigation and accessibility.
 *
 * - `CheckboxField` is essentially an alias for `OptionField`, allowing multiple selections.
 * - `RadioField` is a thin wrapper that restricts selection to a single value.
 *
 * Note that the `value` prop differs between the two:
 *
 * - For `CheckboxField`, `value` is an **array** of selected values.
 * - For `RadioField`, `value` is a **single** selected value.
 *
 * Both components take an `options` prop structured as an array of `{ value, label }` objects:
 *
 *
 * ```tsx
 * <CheckboxField
 *    name="favourite_fruits"
 *    value={["apple", "banana"]}   // <-- An array of values
 *    options={[
 *      { value: "apple", label: "An apple, please." },
 *      { value: "banana", label: "No, I meant banana" },
 *      { value: "carrot", label: "Carrot?", disabled: true },
 *    ]}
 *  />
 * ```
 * ```tsx
 * <RadioField
 *    name="favourite_fruit"
 *    value="apple"                 // <-- A single value
 *    options={[
 *      { value: "apple", label: "Apples, of course!" },
 *      // ...
 *    ]}
 *  />
 * ```
 *
 * The component renders standard html form elements, to ensure keyboard
 * interactions can be handled by the browser (instead of requiring JS).
 */
export default function OptionField<Value>({
  // Base field props
  error,
  showError,
  label,
  disabled,
  required,
  fieldWrapperProps = {},

  // Field specific props
  type,
  values,
  name,
  options,
  onChange = () => {},
  variant = "primary",
  tabIndex,
  className,
  ...fieldsetProps
}: OptionFieldProps<Value>) {
  // Field wrapper and properties for input element
  const {
    FieldWrapper,
    fieldProps: { hasError, ...fieldProps },
  } = useFieldWrapper({
    error,
    showError,
  });

  // Handle change: add/remove the option from the values, depending on
  // whether it is checked
  const handleChange = (newValue: Value, checked: boolean) => {
    if (checked) {
      onChange([...values, newValue]);
    } else {
      onChange(values.filter((v) => v !== newValue));
    }
  };

  return (
    <FieldWrapper
      disabled={disabled}
      required={required}
      {...fieldWrapperProps}
    >
      <fieldset
        className={classNames(
          styles.optionGroup,
          hasError && styles.hasError,
          className
        )}
        {...fieldProps}
        {...fieldsetProps}
      >
        {label && <legend>{label}</legend>}
        {options.map((option, index) => {
          return (
            <Option
              key={option.value}
              type={type}
              name={name}
              value={option.value}
              label={option.label}
              tabIndex={index === 0 ? tabIndex : undefined}
              checked={values.includes(option.value)}
              disabled={disabled || option.disabled}
              onChange={(e) => handleChange(option.value, e.target.checked)}
              variant={variant}
              hasError={hasError}
            />
          );
        })}
      </fieldset>
    </FieldWrapper>
  );
}
