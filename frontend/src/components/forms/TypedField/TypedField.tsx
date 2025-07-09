/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ChangeEvent } from "react";
import Input, { InputProps } from "./Input";
import { useFieldWrapper } from "../FieldWrapper";
import type { BaseFieldProps } from "../types";
import styles from "./TypedField.module.scss";

interface TypedFieldProps extends BaseFieldProps, InputProps {
  /** Name for the the icon shown as prefix (e.g. "globe" for the "fa-globe" icon) */
  iconName?: string;
}

export default function TypedField({
  // Base field props
  error,
  showError,
  label,
  disabled,
  required,
  fieldWrapperProps = {},

  // TypedField specific props
  value,
  maxLength,
  prefix,
  suffix,
  iconName,
  onChange = () => {},
  ...inputProps
}: TypedFieldProps) {
  // Field wrapper and properties for input element
  const { FieldWrapper, fieldProps } = useFieldWrapper({ error, showError });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // TODO use validator
    if (maxLength === undefined || value.length <= maxLength) onChange(value);
  };

  // Icon prefix if an iconName is set
  if (iconName && !prefix) {
    prefix = <span className={`fa fa-${iconName}`} />;
  }

  // Character counter suffix if maxLength is set
  if (maxLength && !suffix) {
    suffix = (
      <span className={styles.charCount}>
        {value?.length ?? 0}/{maxLength}
      </span>
    );
  }

  return (
    <FieldWrapper
      label={label}
      disabled={disabled}
      required={required}
      {...fieldWrapperProps}
    >
      <Input
        value={value}
        onChange={handleChange}
        prefix={prefix}
        suffix={suffix}
        disabled={disabled}
        {...fieldProps}
        {...inputProps}
      />
    </FieldWrapper>
  );
}
