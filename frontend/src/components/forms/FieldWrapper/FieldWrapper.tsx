/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, ReactNode } from "react";

import classNames from "classnames";
import styles from "./FieldWrapper.module.scss";
import { BaseFieldProps } from "../types";

export interface FieldWrapperProps
  extends Omit<BaseFieldProps, "fieldWrapperProps">,
    HTMLAttributes<HTMLDivElement> {
  /** Id for the error message element */
  errorId?: string;

  /** Id for the inpute element */
  fieldId?: string;

  /** Whether to show the error icon */
  showErrorIcon?: boolean;

  /** Whether to show the label. Ignored if `passOnLabel=true`. */
  showLabel?: boolean;

  /** Optional classes to be applied to the label*/
  labelClassName?: string;

  /** Whether to show a flag indicating the field is required. */
  showRequired?: boolean;

  /** Whether to show a flag signalling the field is disabled. */
  showDisabled?: boolean;

  /**
   * The text shown to indicate that a field is disabled.
   * Default `(disabled)`. This is ignored if `showDisabled=false.`
   */
  disabledText?: string | ReactNode;
}

/**
 * The `FieldWrapper` component wraps an input field with a label and
 * an optional error message. To coordinate the references between the label,
 * input, and error, there is a `useFieldWrapper` hook that returns an instance
 * of the component and generates unique identifiers for the error and field
 * element. You should, in short, not use this component directly.
 * A typical use case would look something like this:
 *
 * ```tsx
 *
 * function MyField({
 *    label,
 *    error,
 *    showError,
 *    disabled,
 *    required,
 *    ...inputProps
 * }) {
 *  const { FieldWrapper, ...fieldProps} = useFieldWrapper({ error, showError })
 *  return (
 *    <FieldWrapper label={label} disabled={disabled} required={required}>
 *      <input
 *        type="text"
 *        disabled={disabled}
 *        {...fieldProps}
 *        {...inputProps}
 *      />
 *    </FieldWrapper>
 *  );
 * }
 * ```
 *
 * Optional parameters such as `showDisabled` or `disabledText` allow you
 * to tweak the visual appearance of the label and error message.
 */
export default function FieldWrapper({
  label,
  error,
  disabled,
  required = false,
  errorId,
  fieldId,
  showError = true,
  showErrorIcon = true,
  showLabel = true,
  labelClassName = "",
  showRequired = true,
  showDisabled = true,
  disabledText = "(disabled)",
  className,
  children,
  ...divProps
}: FieldWrapperProps) {
  return (
    <div
      className={classNames(
        styles.fieldWrapper,
        disabled && styles.disabled,
        className
      )}
      {...divProps}
    >
      {showLabel && label && (
        <label
          className={classNames(styles.label, labelClassName)}
          htmlFor={fieldId}
        >
          <span>{label}</span>
          {showRequired && required && (
            <span className={styles.requiredFlag}>*</span>
          )}
          {showDisabled && disabled && (
            <span className={styles.disabledFlag}>{disabledText}</span>
          )}
        </label>
      )}
      {children}
      {showError && error && (
        <p className={styles.error} id={errorId}>
          {showErrorIcon && <span className={styles.errorIcon}>!</span>}
          {error}
        </p>
      )}
    </div>
  );
}
