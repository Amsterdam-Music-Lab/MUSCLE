/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import type { Variant } from "@/types/themeProvider";
import { Children, isValidElement, cloneElement } from "react";
import classNames from "classnames";
import styles from "./InputGroup.module.scss";

export interface InputGroupProps extends HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
  className?: string;
  variant?: Variant;

  /** Whether to try and forward the variant property also to all children */
  forwardVariant?: boolean;

  stretch?: boolean;
}

export default function InputGroup({
  children,
  className,
  variant,
  forwardVariant = true,
  stretch = false,
  ...props
}: InputGroupProps) {
  if (variant && forwardVariant) {
    children = Children.map(children, (child) => {
      if (!isValidElement(child)) return child;
      try {
        return cloneElement(child, { ...(child.props || {}), variant });
      } catch (e) {
        return child;
      }
    });
  }

  return (
    <div
      className={classNames(styles.inputGroup, styles.stretch, className)}
      data-testid="input-group"
      {...props}
    >
      {children}
    </div>
  );
}
