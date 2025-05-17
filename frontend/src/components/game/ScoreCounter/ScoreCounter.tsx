/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { HTMLAttributes } from "react";

import useAnimatedScore from "@/hooks/useAnimatedScore";
import styles from "./ScoreCounter.module.scss";

export interface ScoreCounterProps extends HTMLAttributes<HTMLSpanElement> {
  /**
   * The score to show. This is a number that can be positive, negative, or zero.
   */
  score: number;

  /**
   * Optional label to show after the score (e.g. "points"). Undefined by default.
   */
  label?: string;

  /**
   * Duration of the score animation in milliseconds. Default is 500ms.
   */
  durationMs?: number;

  /**
   * The score to start counting from. Defaults to 0.
   */
  startScore?: number;

  /* Placeholder shown when the scure is undefined (which shouldn't happen). */
  placeholder?: string;
}

/**
 * Shows a score that automatically counts up to the given score. The score itself
 * is an inline-block with fixed width so that it doesn't move while counting.
 */
export default function ScoreCounter({
  score,
  label,
  durationMs = 1000,
  startScore = 0,
  placeholder = "??",
  ...spanProps
}: ScoreCounterProps) {
  const scoreLength = `${score}`.length ?? 0;
  const currentScore = useAnimatedScore(score, { durationMs, startScore });

  return (
    <span data-testid="score" {...spanProps}>
      {score === undefined ? (
        placeholder
      ) : (
        <span className={styles.score} style={{ width: `${scoreLength}ch` }}>
          {currentScore || currentScore === 0 ? currentScore + " " : ""}
        </span>
      )}
      {label && <> {label}</>}
    </span>
  );
}
