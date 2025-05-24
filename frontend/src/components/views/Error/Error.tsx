/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import classNames from "classnames";
import styles from "./Error.module.scss";

export interface ErrorProps extends HTMLAttributes<HTMLDivElement> {
  /** The error message to show */
  message?: string;

  /** Title of the error card */
  title?: string;
}

/**
 * Shows a minimal error page with no dependencies.
 */
export default function Error({
  message,
  title = "An error has occured...",
  className,
  children,
  ...divProps
}: ErrorProps) {
  return (
    <div className={classNames(styles.errorPage, className)} {...divProps}>
      <div className={styles.card}>
        <h1>{title}</h1>
        {message && <p className={styles.message}>{message}</p>}
        {children}
        <p className={styles.footer}>
          Return to the <a href="/">home page</a>.
        </p>
      </div>
    </div>
  );
}
