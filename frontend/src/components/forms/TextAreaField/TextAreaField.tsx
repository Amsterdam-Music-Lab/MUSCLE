/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { FieldOption } from "../types";
import type { HTMLAttributes } from "react";
import type { BaseFieldProps } from "../FieldWrapper";

import classNames from "classnames";
import { useFieldWrapper } from "../FieldWrapper";
import styles from "./TextAreaField.module.scss";

export interface SelectOption<Value> extends FieldOption<Value> {}

export interface TextAreaFieldProps
  extends BaseFieldProps,
    HTMLAttributes<HTMLTextAreaElement> {
  /** Whether the textarea can be resized. Default false.  */
  resizable: boolean;
}

/**
 */
export default function TextAreaField({
  // Default field props
  label,
  error,
  showError,
  disabled,
  required,
  fieldWrapperProps = {},

  // Textarea props
  value,
  resizable = false,
  rows = 3,
  className,
  onChange,
  ...textAreaProps
}: TextAreaFieldProps) {
  const {
    FieldWrapper,
    fieldProps: { hasError, ...fieldProps },
  } = useFieldWrapper({ error, showError });
  return (
    <FieldWrapper
      label={label}
      disabled={disabled}
      required={required}
      {...fieldWrapperProps}
    >
      <textarea
        value={value ?? ""}
        disabled={disabled}
        rows={rows}
        className={classNames(
          styles.textarea,
          hasError && styles.hasError,
          resizable && styles.resizable,
          className
        )}
        onChange={(e) => onChange(e.target.value)}
        {...textAreaProps}
        {...fieldProps}
      />
    </FieldWrapper>
  );
}
