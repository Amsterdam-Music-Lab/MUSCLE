/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import type { Variant } from "@/types/themeProvider";
import classNames from "classnames";
import { renderTemplate } from "@/util/renderTemplate";
import styles from "./ProgressBar.module.scss";

interface ProgressBarProps extends HTMLAttributes<HTMLDivElement> {
  /** The value to show */
  value?: number;

  /** Minimum value (default 0) */
  min?: number;

  /** The maximum value (default 100). */
  max?: number;

  /** A template string for the value, default "{{value}%""} */
  template?: string;

  /** Whether to animate the bar */
  animate?: boolean;

  /** Type of fill */
  variant?: Variant;
}

/**
 * Displays a progress bar.
 */
export default function ProgressBar({
  value = 0,
  min = 0,
  max = 100,
  template = "{{roundedValue}}%",
  animate = true,
  variant = "primary",
  className,
  ...rest
}: ProgressBarProps) {
  const clampedValue = Math.min(Math.max(min, value), max);
  const percentage = Math.round(((clampedValue - min) / (max - min)) * 100);
  const templateData = {
    value: clampedValue,
    roundedValue: Math.round(clampedValue),
    percentage,
    roundedPercentage: Math.round(percentage),
  };
  const label = renderTemplate(template, templateData);
  return (
    <div
      className={classNames(
        styles.progressBar,
        animate && styles.animate,
        "rounded-sm bg-inset-sm",
        className
      )}
      {...rest}
    >
      <div
        className={classNames(`fill-${variant}`, "rounded-sm small")}
        role="progressbar"
        data-testid="progressbar"
        style={{ width: `${percentage}%` }}
        aria-valuenow={clampedValue}
        aria-valuemin={min}
        aria-valuemax={max}
      >
        {label}
      </div>
    </div>
  );
}
