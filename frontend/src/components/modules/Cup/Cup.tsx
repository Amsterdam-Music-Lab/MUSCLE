/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, CSSProperties } from "react";
import { useLingui } from "@lingui/react/macro";
import classNames from "classnames";
import styles from "./Cup.module.scss";

export type CupType =
  | "diamond"
  | "platinum"
  | "gold"
  | "silver"
  | "bronze"
  | "plastic";

export interface CupProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * The type of cup to show: "diamond", "platinum", "gold", "silver", "bronze" or "plastic". The default is "plastic".
   */
  type?: CupType;

  /**
   * An optional label to show below the cup, inside the circle. You can
   * pass a custom label, or `false` if you want to hide the label. By default,
   * the capitalized type (e.g. "Gold") is used as the label.
   */
  label?: string | boolean;

  /** Size of the circle in px */
  radius?: number;

  /**
   * Whether to show a halo around the circle containing the cup.
   */
  showHalo?: boolean;

  /**
   * Whether to animate the cup. This rotates the crown, if any, and
   * will bounce the cup up and down.
   */
  animate?: boolean;

  /**
   * Whether to show the label in uppercase. Default true
   */
  uppercase?: boolean;
}

/**
 * A medal with a cup inside. The cup can be of different types, corresponding
 * to different colors, and the cup can be animated. The cup can also have a label.
 */
export default function Cup({
  type = "plastic",
  label,
  radius = 150,
  showHalo = true,
  animate = true,
  uppercase = true,
  className,
  style,
  ...divProps
}: CupProps) {
  const { t } = useLingui();
  if (label === undefined || label === true) {
    const cupLabels: Record<CupType, string> = {
      diamond: t`Diamond`,
      platinum: t`Platinum`,
      gold: t`Gold`,
      silver: t`Silver`,
      bronze: t`Bronze`,
      plastic: t`Plastic`,
    };
    label = cupLabels[type];
  }
  return (
    <div
      className={classNames(
        styles.cupContainer,
        animate && styles.animate,
        className
      )}
      style={{ "--cup-radius": `${radius}px`, ...style } as CSSProperties}
      {...divProps}
    >
      <div
        className={classNames(
          styles.circle,
          showHalo && styles.halo,
          styles[type],
          label && styles.offset
        )}
        data-testid="cup"
      >
        <div className={styles.cup} data-testid="cup-animation" />
        {label && (
          <div
            className={classNames(styles.label, uppercase && styles.uppercase)}
            data-testid="cup-text"
          >
            {label}
          </div>
        )}
        {showHalo && <div className={styles.rays} />}
      </div>
    </div>
  );
}
