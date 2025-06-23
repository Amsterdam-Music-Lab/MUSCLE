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

interface TrackProps extends HTMLAttributes<HTMLDivElement> {
  props: HTMLAttributes<HTMLDivElement>;
}

export default function Track({ children, props }: TrackProps) {
  return (
    <div className={classNames(styles.track)}>
      <div className={classNames(styles.trackInner)} {...props}>
        {children}
      </div>
    </div>
  );
}
