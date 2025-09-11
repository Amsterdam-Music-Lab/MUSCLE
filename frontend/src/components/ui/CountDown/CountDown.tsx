/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { HTMLAttributes } from "react";
import { useState, useEffect } from "react";
import Timer from "@/util/timer";

export interface CountdownProps extends HTMLAttributes<HTMLSpanElement> {
  /** Duration of the count  down */
  duration: number;

  /** Whether the timer is running */
  running?: boolean;
}

// TODO note the component files are capitzalized wrongly
// (Countdown is one word)

/**
 * Renders a simple span that counts down for a certain number
 * of seconds. The data-status attribute can take the values
 * "running", "paused" or "finished" and can be used to style the
 * component.
 */
export default function Countdown({
  duration,
  running = true,
  ...spanProps
}: CountdownProps) {
  const [time, setTime] = useState(0);
  const [finished, setFinished] = useState(false);

  useEffect(() => {
    if (!running) return;
    return Timer({
      duration,
      onTick: (t) => setTime(Math.min(t, duration)),
      onFinish: () => setFinished(true),
    });
  }, [duration, running]);

  return (
    <span
      data-status={finished ? "finished" : running ? "running" : "paused"}
      {...spanProps}
    >
      {finished ? "0" : Math.ceil(duration - time)}
    </span>
  );
}
