/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import type { FieldOption } from "../types";
import classNames from "classnames";
import { Variant } from "@/types/themeProvider";
import styles from "./Option.module.scss";
import "@/scss/theme.scss";
import "@/scss/forms.scss";

interface OptionProps<Value>
  extends FieldOption<Value>,
    HTMLAttributes<HTMLLabelElement> {
  name: string;
  onChange: () => void;
  checked?: boolean;
  variant?: Variant;
  type: "radio" | "checkbox";
  hasError?: boolean;
}

function Option<Value>({
  name,
  type,
  value,
  label,
  checked,
  onChange,
  variant = "primary",
  disabled = false,
  className,
  hasError,
}: OptionProps<Value>) {
  return (
    <label
      className={classNames(
        styles.option,
        checked && styles.checked,
        disabled && styles.disabled,
        hasError && styles.hasError,
        className
      )}
    >
      <input
        type={type}
        name={name}
        value={value}
        checked={checked}
        onChange={onChange}
        disabled={disabled}
        className="hidden-input"
      />
      <div className={styles.focusRing}>
        <i
          className={classNames(
            styles.handle,
            styles[type],
            checked && `fill-${variant}`
          )}
        />
        <span className={styles.label}>{label ?? value}</span>
      </div>
    </label>
  );
}

export default Option;
