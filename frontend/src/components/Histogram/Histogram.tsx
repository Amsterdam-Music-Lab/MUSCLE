/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { FC, useEffect, useRef, useState } from "react";
import useBoundStore from "@/util/stores";
import { BarPlot, BarPlotProps } from "@/components/game";

export interface HistogramProps
  extends Omit<BarPlotProps, "data" | "min" | "max"> {
  /** The number of bars in the histogram */
  bars?: number;

  /** Whether the histogram is being updated */
  running?: boolean;

  /**
   * Whether to randomize bar heights. If no buffer is present, the
   * histogram will also be random.
   */
  random?: boolean;

  /**
   * If `random` is `true`, this prop sets the update interval in milliseconds.
   * Default is 100 ms. Ignored when `random` is `false`.
   */
  interval?: number;
}

/**
 * A continuously updated histogram showing either random data
 * or the frequency data from the audio context. Note that the
 * component mostly provides the frequency data, the actual visualization
 * is handled by the BarPlot component.
 */
const Histogram: FC<HistogramProps> = ({
  bars = 8,
  running = true,
  random = false,
  interval = 200,
  ...props
}) => {
  const [data, setData] = useState<Uint8Array>(new Uint8Array(bars));
  const currentAction = useBoundStore((state) => state.currentAction);
  const animationFrameRef = useRef<number>();
  const intervalRef = useRef<number>();

  const isBuffer = currentAction?.playback?.play_method === "BUFFER";
  const randomize = random || !isBuffer;

  const stopAnimation = () => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
  };

  const stopInterval = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  useEffect(() => {
    if (!running) {
      stopAnimation();
      stopInterval();
      setData(new Uint8Array(bars));
      return;
    }

    // Update the histogram data
    const update = () => {
      let newData: Uint8Array;

      if (randomize) {
        // Generate random frequency data
        newData = new Uint8Array(bars);
        for (let i = 0; i < bars; i++) {
          newData[i] = Math.floor(Math.random() * 256);
        }
        setData(newData);
      } else if (window.audioContext && window.analyzer) {
        const freqData = new Uint8Array(bars + 3);
        window.analyzer.getByteFrequencyData(freqData);
        // Remove the lower end of the frequency data
        newData = freqData.slice(3, bars + 3);
        setData(newData);
        animationFrameRef.current = requestAnimationFrame(update);
        return; // Exit the function to prevent setting another interval
      } else {
        newData = new Uint8Array(bars);
        setData(newData);
      }
    };

    if (randomize) {
      stopInterval();
      intervalRef.current = window.setInterval(update, interval);
    } else {
      stopAnimation();
      animationFrameRef.current = requestAnimationFrame(update);
    }

    return () => {
      stopAnimation();
      stopInterval();
    };
  }, [running, bars, randomize, interval]);

  return <BarPlot data={[...data]} min={0} max={255} {...props} />;
};

export default Histogram;
