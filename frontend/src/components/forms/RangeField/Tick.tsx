/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";
import classNames from "classnames";
import styles from "./RangeField.module.scss";

export interface TickProps extends HTMLAttributes<HTMLDivElement> {
  label?: string;
  props: HTMLAttributes<HTMLDivElement>;
}

export default function Tick({ props, label, className, ...divProps }) {
  return (
    <div
      className={classNames(styles.tick, className)}
      {...props}
      {...divProps}
    >
      <div className={styles.tickMark} />
      <div className={styles.tickLabel}>{label}</div>
    </div>
  );
}
