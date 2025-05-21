/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import classNames from "classnames";

interface DevCardLabelProps extends HTMLAttributes<HTMLDivElement> {}

/**
 * A component that shows card labels, but only in development
 */
export default function DevCardLabel({
  style,
  className,
  children,
  ...divProps
}: DevCardLabelProps) {
  return (
    children !== undefined &&
    import.meta.env.DEV && (
      <div
        style={{ opacity: 0.5, ...style }}
        className={classNames(
          "text-light d-flex flex-column justify-content-center small",
          className
        )}
        {...divProps}
      >
        {children}
      </div>
    )
  );
}
