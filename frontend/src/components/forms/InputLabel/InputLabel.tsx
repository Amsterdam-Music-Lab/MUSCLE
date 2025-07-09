/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { LabelHTMLAttributes, ReactNode } from "react";
import type { Variant } from "@/types/themeProvider";
import classNames from "classnames";
import styles from "./InputLabel.module.scss"; // optional

export interface InputLabelProps extends LabelHTMLAttributes<HTMLLabelElement> {
  htmlFor?: string;
  className?: string;
  children: ReactNode;
  variant?: Variant;
}

export default function InputLabel({
  htmlFor,
  className,
  children,
  variant,
  ...props
}: InputLabelProps) {
  return (
    <label
      htmlFor={htmlFor}
      className={classNames(styles.label, className)}
      {...props}
    >
      <span className={classNames(variant && `text-fill-${variant}`)}>
        {children}
      </span>
    </label>
  );
}
