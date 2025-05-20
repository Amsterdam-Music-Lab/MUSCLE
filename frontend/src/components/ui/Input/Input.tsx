/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { ChangeEvent, InputHTMLAttributes } from "react";

import { useState, forwardRef } from "react";
import classNames from "classnames";
import styles from "./Input.module.scss";

export interface InputProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, "onChange" | "value"> {
  value?: string;
  className?: string;
  onChange?: (e: ChangeEvent) => void;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      value: initValue = "",
      onChange: handleChange = () => {},
      ...props
    },
    ref
  ) => {
    const [value, setValue] = useState(initValue);
    return (
      <input
        ref={ref}
        type="text"
        value={value}
        onChange={(e) => {
          handleChange(e);
          setValue(e.target.value);
        }}
        className={classNames(styles.input, className)}
        {...props}
      />
    );
  }
);

export default Input;
