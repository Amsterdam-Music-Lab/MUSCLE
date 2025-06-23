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
  return (
    <div
      className={classNames(
        styles.thumb,
        isDragged & styles.dragging,
        className
      )}
      {...props}
      {...divProps}
    >
      {label && <div className={styles.thumbLabel}>{label}</div>}
    </div>
  );
}
