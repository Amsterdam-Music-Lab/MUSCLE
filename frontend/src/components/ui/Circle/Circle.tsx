/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes, CSSProperties } from "react";

import { useEffect, useState } from "react";
import classNames from "classnames";
import Timer from "@/util/timer";
import styles from "./Circle.module.scss";

export interface CircleProps extends HTMLAttributes<HTMLDivElement> {
  startTime?: number;
  duration?: number;
  color?: string;
  onTick?: (time: number) => void;
  onFinish?: () => void;
  radius?: number;
  strokeWidth?: number;
  running?: boolean;
  animateCircle?: boolean;
  rotate?: boolean;
}

/**
 * Circle shows a counterclockwise circular animation
 */
export default function Circle({
  startTime = 0,
  duration = 0,
  color = "white",
  onTick,
  onFinish,
  radius = 60,
  strokeWidth = 1.5,
  running = true,
  animateCircle = true,
  rotate = false,
  children,
  className,
  style: customStyles,
  ...divProps
}: CircleProps) {
  // automatic timer
  const [time, setTime] = useState(startTime);

  // Time animation
  useEffect(() => {
    if (!running) {
      return;
    }

    // Create timer and return stop function
    return Timer({
      time: startTime,
      duration,
      onTick: (t) => {
        setTime(Math.min(t, duration));
        onTick && onTick(t);
      },
      onFinish: () => {
        onFinish && onFinish();
      },
    });
  }, [running, duration, onTick, onFinish, startTime]);

  const diameter = radius * 2;
  const circumference = diameter * Math.PI;
  const size = diameter + strokeWidth;
  let style = {};
  if (animateCircle) {
    const perc = duration
      ? Math.min(1, (time + (running || time > 0 ? 0.1 : 0)) / duration)
      : 0;
    style = {
      strokeDasharray: circumference + " " + circumference,
      strokeDashoffset: perc * circumference,
    };
  }
  // while running, add 0.1 to compensate for the css transition delay
  return (
    <div
      className={classNames(styles.circle, rotate && styles.rotate, className)}
      style={
        {
          width: size,
          height: size,
          ...customStyles,
        } as CSSProperties
      }
      data-testid="circle"
      {...divProps}
    >
      <svg
        width={size}
        height={size}
        viewBox={"0 0 " + size + " " + size}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          opacity="0.25"
          cx={radius + strokeWidth / 2}
          cy={radius + strokeWidth / 2}
          r={radius}
          stroke="white"
          strokeWidth={strokeWidth}
        />
        <circle
          className={styles.circlePercentage}
          cx={radius + strokeWidth / 2}
          cy={radius + strokeWidth / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          style={style}
        />
      </svg>
      {children && <div className={styles.children}>{children}</div>}
    </div>
  );
}
