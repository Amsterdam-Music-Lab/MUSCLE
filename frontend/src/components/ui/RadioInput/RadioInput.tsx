/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import classNames from "classnames";
import styles from "./RadioInput.module.scss";
import { Variant } from "@/types/themeProvider";
import "@/scss/theme.scss";

interface RadioInputProps<Value> extends HTMLAttributes<HTMLDivElement> {
  /** The current value */
  value?: Value;

  /** A list of values.  */
  values: Value[];

  /**
   * A list of labels, should have the same length as values. If no labels
   * are provided, the values are used as labels.
   */
  labels?: string[];

  /** Event handler called whenever the selection changes. */
  onChange?: (value: Value) => void;

  variant?: Variant;
}

/**
 * Radio Input allows users to select one out of a list of options.
 */
export default function RadioInput<Value>({
  value: currentValue,
  values,
  labels,
  onChange = () => {},
  className,
  variant = "primary",
  ...divProps
}: RadioInputProps<Value>) {
  if (!values || Object.keys(values).length <= 0) {
    throw new Error("Radio inputs must have values");
  }
  if (!labels || labels.length === 0) {
    labels = [...values];
  }
  if (values.length !== labels.length) {
    throw new Error("Please provide as many labels as values");
  }

  return (
    <div className={classNames(styles.radioInput, className)} {...divProps}>
      {values.map((value, index) => {
        const checked = currentValue === value;
        return (
          <div
            key={value}
            className={classNames(styles.option, checked && styles.checked)}
            onClick={() => onChange(value)}
            onKeyDown={() => onChange(value)}
            aria-checked={checked}
            tabIndex={index}
            role="radio"
          >
            <i
              className={classNames(
                styles.handle,
                checked && `fill-${variant}`
              )}
            ></i>
            <span className={styles.label}>{labels[index]}</span>
          </div>
        );
      })}
    </div>
  );
}
