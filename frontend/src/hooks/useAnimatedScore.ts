/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useEffect, useState } from "react";

interface UseAnimatedScoreProps {
  /** The duration of the animation in ms */
  durationMs?: number;

  /** The score to start counting from. Defaults to 0*/
  startScore?: number;
}

/**
 * A hook that animates a score from the current score to the target score,
 * in a given duration. The hook returns the current score, which is updated
 * every frame until the target score is reached. The starting score can also
 * be set, but defaults to 0.
 */
export default function useAnimatedScore(
  targetScore: number,
  { durationMs = 500, startScore = 0 }: UseAnimatedScoreProps = {}
) {
  const [score, setScore] = useState(startScore);

  useEffect(() => {
    if (targetScore === score) return;

    let animationFrameId: number;
    const startTime = performance.now();
    const difference = targetScore - score;

    const step = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / durationMs, 1);
      const nextScore = Math.round(score + difference * progress);
      setScore(nextScore);

      if (progress < 1) {
        animationFrameId = requestAnimationFrame(step);
      }
    };

    animationFrameId = requestAnimationFrame(step);

    return () => cancelAnimationFrame(animationFrameId);
  }, [targetScore, durationMs, score]);

  return score;
}
