/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, ReactNode } from "react";
import { useState } from "react";
import classNames from "classnames";
import styles from "./Input.module.scss";
import { FieldWrapperChildProps } from "../Field";

export interface InputProps
  extends Omit<HTMLAttributes<HTMLInputElement>, "value">,
    FieldWrapperChildProps {
  prefix?: string | ReactNode;
  suffix?: string | ReactNode;
  divProps?: HTMLAttributes<HTMLDivElement>;
}

export default function Input({
  type = "text",
  hasError,
  name,
  value,
  maxLength,
  className,
  disabled,
  autoFocus = true,
  prefix,
  suffix,
  onFocus,
  onBlur,
  divProps = {},
  ...inputProps
}: InputProps) {
  const [isFocused, setIsFocused] = useState(false);
  return (
    <div
      className={classNames(
        styles.inputContainer,
        isFocused && styles.focused,
        suffix && styles.hasSuffix,
        disabled && styles.disabled,
        hasError && styles.hasError,
        className
      )}
      {...divProps}
    >
      {prefix && <div className={styles.prefix}>{prefix}</div>}
      <input
        type={type}
        name={name}
        value={value ?? ""}
        maxLength={maxLength}
        className={styles.input}
        disabled={disabled}
        autoFocus={autoFocus}
        onFocus={(e) => {
          setIsFocused(true);
          if (onFocus) onFocus(e);
        }}
        onBlur={(e) => {
          setIsFocused(false);
          if (onBlur) onBlur(e);
        }}
        {...inputProps}
      />
      {suffix && <div className={styles.suffix}>{suffix}</div>}
    </div>
  );
}
