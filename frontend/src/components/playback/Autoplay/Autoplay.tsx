/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";

import { useEffect, useState } from "react";
import classNames from "classnames";
import { Circle, Countdown } from "@/components/ui";
import { Spectrum } from "../Spectrum";
import styles from "./Autoplay.module.scss";

export interface AutoplayProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * The duration of the autoplay. (Formerly called responseTime)
   */
  duration: number;

  /** A message shown below the progress. */
  message?: string;

  playSection: (section: number) => void;

  /** Callback called when Autoplay is finished */
  onFinish: () => void;

  /** The color to use. This is passed on to the circle and spectrum. */
  color?: string;

  /** The interval with which the spectrum is updated. Default 400ms */
  spectrumIntervalMs?: number;

  /** Whether to animate the circle. Default true. */
  animateCircle?: boolean;

  /** Classname of the icon. Default "fa-headphones" */
  icon?: string;

  /** Whether to show the spectrum */
  showSpectrum?: boolean;

  /** Whether to show the countdown */
  showCountdown?: boolean;

  // TODO what is this doing?!
  startedPlaying?: boolean;
}

export default function Autoplay({
  message,
  playSection,
  onFinish,
  duration,
  spectrumIntervalMs = 400,
  animateCircle = true,
  icon = "fa-headphones",
  color = "black",
  showSpectrum = true,
  showCountdown = true,
  className,
  startedPlaying, // TODO what is this doing?!
  ...divProps
}: AutoplayProps) {
  const [running, setRunning] = useState(true);
  useEffect(() => playSection(0), [playSection, startedPlaying]);

  const hasSpectrum = showSpectrum;
  const hasCountdown = duration && showCountdown;

  return (
    <div className={classNames(styles.autoplay, className)} {...divProps}>
      <Circle
        running={running}
        duration={duration}
        color={color}
        animateCircle={animateCircle}
        onFinish={() => {
          setRunning(false);
          onFinish();
        }}
        className={styles.circle}
      >
        {hasSpectrum && (
          <Spectrum
            running={running}
            className={styles.spectrum}
            interval={spectrumIntervalMs}
            color={color}
          />
        )}
        {!hasSpectrum && hasCountdown && (
          <Countdown
            duration={duration}
            running={running}
            className={styles.countdown}
          />
        )}
        {!hasSpectrum && !hasCountdown && (
          <div className={styles.icon}>
            <span className={classNames(icon, "fa-solid fa-6x")} />
          </div>
        )}
      </Circle>

      {message && <p className={classNames(styles.message)}>{message}</p>}
    </div>
  );
}
