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

export interface ThumbProps extends HTMLAttributes<HTMLDivElement> {
  isDragged: boolean;
  props: HTMLAttributes<HTMLDivElement>;
  label?: string;
}

export default function Thumb({
  isDragged,
  props,
  label,
  className,
  ...divProps
}) {
  const value = props["aria-valuenow"];
  const min = props["aria-valuemin"];
  const max = props["aria-valuemax"];
  const relPos = (value - min) / (max - min);
  return (
    <div
      className={classNames(
        styles.thumb,
        isDragged & styles.dragging,
        relPos < 0.5 ? styles.left : styles.right,
        className
      )}
      {...props}
      {...divProps}
    >
      {label !== undefined && <div className={styles.thumbLabel}>{label}</div>}
    </div>
  );
}
