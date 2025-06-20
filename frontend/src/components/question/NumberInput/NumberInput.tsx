/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { KeyboardEvent, ChangeEvent, HTMLAttributes } from "react";
import { forwardRef } from "react";
import classNames from "classnames";
import styles from "./NumberInput.module.scss";

interface NumberInputProps
  extends Omit<
    HTMLAttributes<HTMLInputElement>,
    "type" | "onChange" | "value"
  > {
  value?: number;
  onChange: (value: number | undefined) => void;
}

/**
 * Number input
 */
const NumberInput = forwardRef<HTMLInputElement, NumberInputProps>(
  (
    {
      value,
      min,
      max,
      onChange = () => {},
      onKeyDown = () => {},
      autoFocus = true,
      className,
      ...inputProps
    },
    ref
  ) => {
    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
      const strValue = e.target.value;
      if (strValue === "") return onChange(undefined);
      const numValue = Number(strValue);
      if (isNaN(numValue)) return;
      if (
        (min !== undefined && numValue < min) ||
        (max !== undefined && numValue > max)
      ) {
        return;
      }
      onChange(numValue);
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter") e.preventDefault();
      onKeyDown(e);
    };

    return (
      <input
        type="number"
        value={value ?? ""}
        autoFocus={autoFocus}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        className={classNames(styles.numberInput, className)}
        min={min}
        max={max}
        {...inputProps}
      />
    );
  }
);

export default NumberInput;
