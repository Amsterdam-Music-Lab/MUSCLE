/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import type { CSSProperties } from "react";
import type { Variant } from "@/types/themeProvider";
import type {
  BaseTimeline,
  TimelineConfig,
  TimelineStep,
} from "@/types/timeline";
import type { Fill } from "@/types/svg";

import classNames from "classnames";
import { symbols as svgSymbols } from "@/components/svg";
import { useVariantFill } from "@/hooks/useVariantFill";
import styles from "./Timeline.module.scss";

interface ProcessTimelineConfigProps extends BaseTimeline {
  timeline: TimelineConfig;
}

/**
 * Utility function that returns a timeline configuration object from a
 * sequence of timeline symbols. A timeline configuration is simply a list
 * of objects that define the symbol, its size, whether it is a trophy and
 * whether it should be animated.
 */
export function processTimelineConfig({
  timeline,
  dotSize = 10,
  trophySize,
  showDots = true,
  variant,
  fill,
  animate,
}: ProcessTimelineConfigProps): TimelineStep[] {
  // Make sure all defaults are defined on the timeline object.
  timeline = {
    dotSize,
    trophySize: trophySize || dotSize * 3,
    showDots,
    variant,
    fill,
    animate,
    ...timeline,
  } as TimelineConfig;
  trophySize = timeline?.trophySize ?? (trophySize || dotSize * 3);

  let steps;
  if ("symbols" in timeline) {
    steps = timeline.symbols.map((symbol) => ({ symbol } as TimelineStep));
  } else {
    steps = timeline.steps;
  }

  return steps.map((step) => {
    const defaultStep = {
      trophy: step.symbol !== "dot",
      size: step.symbol === "dot" ? timeline.dotSize : timeline.trophySize,
    } as Partial<TimelineStep>;
    if (timeline.animate)
      defaultStep.animate = step.symbol === "dot" ? false : timeline.animate;
    if (timeline.fill) defaultStep.fill = fill;
    if (timeline.variant) defaultStep.variant = variant;
    const updated = { ...defaultStep, ...step };
    if (timeline.showDots === false && step.symbol === "dot") {
      updated.symbol = undefined;
    }
    return updated as TimelineStep;
  });
}

export interface TimelineProps
  extends Omit<ProcessTimelineConfigProps, "timeline" | "animate"> {
  /**
   * A timeline configuration object. See Component documentation for details.
   */
  timeline: TimelineConfig;

  /**
   * Fill of past symbols: everything up to and including the current step.
   * If timeline.fill is defined, that value is used.
   * */
  fillPast?: Fill;

  /** Fill of the future steps: everything after the current step */
  fillFuture?: Fill;

  /** The background of the 'past' spine. If fillPast is a string, spineBgPast defaults to that. */
  spineBgPast?: string;

  /** The background of the 'future' spine. If fillFuture is a string, spineBgFuture defaults to that. */
  spineBgFuture?: string;

  /** Animate the symbols? */
  animate?: boolean;

  /** Whether to show the spine (the line through the timeline) */
  showSpine?: boolean;

  /** Whether to show the symbols at all (or just the spine) */
  showSymbols?: boolean;

  /**
   * Theme variant. If set, this overrides fillPast.
   * If timeline.variant is defined, that is used.
   */
  variant?: Variant;
}

/**
 * Shows a responsive timeline with customizable steps. A timeline is
 * specified by a `TimelineConfig` object:
 *
 * ```ts
 * const timelineConfig = {
 *  // Option 1: configure all steps individually
 *  steps: [
 *      { symbol: "dot", size: 10, ... },
 *      { symbol: "star-4", size: 20, ... },
 *  ],
 *
 *  // Option 2: alternatively, specify only the symbols,
 *  // use the same default config (see below) for all steps.
 *  symbols: ['dot', 'dot', 'star-4', 'dot', ...],
 *
 *  // The current active step.
 *  currentStep: 5,
 *
 *  // Args below are optional and used as defaults for each of the steps:
 *  dotSize: 10,
 *  trophySize: number, // Size of trophy's (non-dots)
 *  showDots: true, // Whether to show the dots
 *  variant: "primary", // Theme variant. If set, this should override the fill.
 *  fill: {
 *   startColor: "#ff0000",
 *   endColor: "#00ff00",
 *  },
 *  animate: true,
 * }
 * ```
 */
export default function Timeline({
  timeline,
  fillPast,
  fillFuture = "#eeeeee",
  spineBgPast,
  spineBgFuture,
  animate = true,
  showSpine = true,
  showDots = true,
  dotSize = 10,
  trophySize,
  showSymbols = true,
  variant,
}: TimelineProps) {
  if (!timeline) {
    throw new Error("Timeline: No timeline provided");
  }

  const steps = processTimelineConfig({
    timeline,
    animate,
    showDots,
    dotSize,
    trophySize,
  });

  const currentStep = timeline.currentStep;
  if (currentStep && currentStep > steps.length) {
    console.warn(
      `Current step (${currentStep}) exceeds the length of the timeline (${steps.length}).`
    );
  }

  const variantFill =
    useVariantFill(timeline.variant ?? variant ?? "primary") ?? "#000";
  fillPast = timeline.fill ?? fillPast ?? variantFill;

  // Determine default bg fill of the spine:
  // Use the fillPast/future colors if they are strings,
  // or make a gradient otherwise.
  if (!spineBgPast) {
    if (typeof fillPast == "string") {
      spineBgPast = fillPast;
    } else {
      spineBgPast = `linear-gradient(90deg, ${fillPast.startColor} -300%, ${fillPast.endColor} 300%)`;
    }
  }
  if (!spineBgFuture) {
    if (typeof fillFuture == "string") {
      spineBgFuture = fillFuture;
    } else {
      spineBgFuture = `linear-gradient(90deg, ${fillFuture.startColor} -200%, ${fillFuture.endColor} 200%)`;
    }
  }

  const style = {
    "--spine-bg-past": spineBgPast,
    "--spine-bg-future": spineBgFuture,
  } as CSSProperties;

  return (
    <div className={styles.timeline} style={style}>
      {steps.map((step, idx) => {
        const Symbol = step.symbol ? svgSymbols[step.symbol] : null;
        return (
          <div className={styles.step} key={idx}>
            {showSymbols && Symbol && (
              <div className={styles.symbol}>
                <Symbol
                  size={step.size}
                  fill={idx < currentStep ? step?.fill ?? fillPast : fillFuture}
                  animate={
                    step.animate !== undefined
                      ? animate && step.animate
                      : animate
                  }
                  style={{ top: `-${(step.size ?? dotSize) / 2}px` }}
                />
              </div>
            )}
            {showSpine && idx >= 1 && (
              <div
                className={classNames(
                  styles.spineSegment,
                  idx < currentStep && styles.active
                )}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
