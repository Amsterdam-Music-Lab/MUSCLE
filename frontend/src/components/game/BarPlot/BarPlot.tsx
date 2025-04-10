/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React from 'react';
import classNames from 'classnames';
import { Variant } from '@/theme/themes';

import styles from "./BarPlot.module.scss"

export interface BarPlotProps extends React.HTMLAttributes<HTMLDivElement> {
  /** An array of numbers */
  data: number[];

  /** The minimum value. If none is given, the lowest value is used */
  min?: number;

  /** The maximumv alue. If none is given, the highest value is used. */
  max?: number
  
  /** The color of the bars.*/
  color?: string

  /** The theme variant (default primary) only used when color is not specified. */
  variant?: Variant;
}

/**
 * A bar plot component. It takes an array of numbers and displays those 
 * as a bar plot. The height of the bars is calculated based on the min and max values.
 * The min and max values are optional. If none are given, the lowest and highest values 
 * in the data array are used. The color of the bars can be specified. If none is given, 
 * the theme variant is used.
 */
export default function BarPlot({
  data, 
  min, 
  max, 
  variant='primary',
  color,
}: BarPlotProps) {
  min = min === undefined ? Math.min(...data) : min;
  max = max === undefined ? Math.max(...data) : max;
  const bars = data.map((val: number) => (val - min) / (max - min) * 100);
  return (
    <div
      className={styles.plot}
      style={{ "--num-bars": bars.length, "--bar-color": color }}
    >
      {bars.map((height, index) => (
        <div key={index} className={styles.column}>
          <div className={classNames(styles.bar, !color && `fill-${variant}`)} style={{height: `${height}%` }} />
        </div>
      ))}
    </div>
  );
};