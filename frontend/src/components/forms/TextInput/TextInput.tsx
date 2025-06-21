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
import styles from "./TextInput.module.scss";

interface TextInputProps
  extends Omit<HTMLAttributes<HTMLInputElement>, "type" | "onChange"> {
  onChange: (value: string) => void;
  className?: string;
}

/**
 * TextInput with a maximum length
 */
const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
  (
    {
      value,
      maxLength,
      onChange = () => {},
      onKeyDown = () => {},
      autoFocus = true,
      className,
      ...inputProps
    },
    ref
  ) => {
    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      if (maxLength === undefined || value.length <= maxLength) onChange(value);
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter") e.preventDefault();
      onKeyDown(e);
    };

    return (
      <div className={classNames(styles.container, className)}>
        <input
          ref={ref}
          type="text"
          value={value ?? ""}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          maxLength={maxLength}
          autoFocus={autoFocus}
          {...inputProps}
        />
        {maxLength && (
          <span className={styles.charCount}>
            {value?.length ?? 0}/{maxLength}
          </span>
        )}
      </div>
    );
  }
);

export default TextInput;
