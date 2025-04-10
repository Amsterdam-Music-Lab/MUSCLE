/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import classNames from "classnames"
import { Star, Dot, Fill } from "@/components/svg";
import styles from "./Timeline.module.scss"
import { type Variant } from "@/theme/themes";
import { getVariantFill } from "@/util/getVariantFill";

type TimelineSymbolName = 'dot' | 'star' | 'star-4' | 'star-5' | 'star-6' | 'star-7' | null;

export const TIMELINE_SYMBOLS = {
  'dot': ({ ...props }) => <Dot {...props} />,
  'star': ({ ...props }) => <Star numPoints={5} {...props} />,
  'star-4': ({ ...props }) => <Star numPoints={4} {...props} />,
  'star-5': ({ ...props }) => <Star numPoints={5} {...props} />,
  'star-6': ({ ...props }) => <Star numPoints={6} {...props} />,
  'star-7': ({ ...props }) => <Star numPoints={7} {...props} />,
  'star-8': ({ ...props }) => <Star numPoints={8} {...props} />
}

export type TimelineConfig = Array<{
  symbol: TimelineSymbolName,
  size: number,
  animate: boolean,
  trophy: boolean
}>

interface GetTimelineProps {
  /** A list of symbol names such as ["dot", "star-4", "dot", ...]  */
  symbols: Array<TimelineSymbolName>;

  /** Size of the dots */
  dotSize?: number;

  /** Size of the trophies (not-dots) */
  trophySize?: number;

  /** Animate the trophies? */
  animate?: boolean;

  /** Show dots at all */
  showDots?: boolean;
}

/**
 * Utility function that returns a timeline configuration object from a
 * sequence of timeline symbols. A timeline configuration is simply a list 
 * of objects that define the symbol, its size, whether it is a trophy and 
 * whether it should be animated.
 */
export function getTimeline({
  symbols,
  dotSize=10,
  trophySize,
  animate=false,
  showDots=true
}: GetTimelineProps): TimelineConfig {
  trophySize = trophySize || dotSize * 3;
  const dotSymbol = showDots ? "dot" : null
  return symbols.map(symbol => ({
    symbol: symbol == "dot" ? dotSymbol : symbol,
    size: symbol == "dot" ? dotSize : trophySize,
    trophy: symbol !== "dot",
    animate: symbol == "dot" ? false : animate,
  }))
}

interface TimelineProps {
  /** 
   * A timeline configuration object. This should be a list of objects specifying
   * the symbol name, the size, whether it is a trophy and whether it is animated.
   * A configuration object can be created using the getTimeline function.
   */
  timeline: TimelineConfig;

  /** The current step in the timeline */
  step: number;

  /** Fill of past symbols: everything up to and including the current step */
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

  /** Theme variant. If set, this overrides fillPast. */
  variant?: Variant;
}

/**
 * Shows a responsive timeline with customizable steps.
 */
export default function Timeline({
  timeline,
  step = 0,
  fillPast = "#000000",
  fillFuture = "#eeeeee",
  spineBgPast,
  spineBgFuture,
  animate = true,
  showSpine = true,
  showSymbols = true,
  variant="primary",
}: TimelineProps) {
  if(variant){
    fillPast = getVariantFill(variant);
  }
  // Determine default bg fill of the spine:
  // Use the fillPast/future colors if they are strings, 
  // or make a gradient otherwise.
  if(!spineBgPast) {
    if(typeof(fillPast) == "string") {
      spineBgPast = fillPast
    } else {
      spineBgPast = `linear-gradient(90deg, ${fillPast.startColor} -300%, ${fillPast.endColor} 300%)`
    }
  }
  if(!spineBgFuture) {
    if(typeof(fillFuture) == "string") {
      spineBgFuture = fillFuture
    } else {
      spineBgFuture = `linear-gradient(90deg, ${fillFuture.startColor} -200%, ${fillFuture.endColor} 200%)`
    }
  }

  return (
    <div className={styles.timeline} style={{
      '--spine-bg-past': spineBgPast, '--spine-bg-future': spineBgFuture
    }}>
      {timeline.map((symbol, idx) => {
        const Symbol = symbol.symbol ? TIMELINE_SYMBOLS[symbol.symbol] : null;
        return (
          <div className={styles.step} key={idx}>
            {showSymbols && Symbol && (
              <div className={styles.symbol}>
                <Symbol
                  size={symbol.size}
                  fill={idx < step ? fillPast : fillFuture}
                  animate={animate && symbol.animate}
                  style={{ top: `-${symbol.size / 2}px` }}
                />
              </div>
            )}
            {showSpine && idx >= 1 && (
              <div className={classNames(styles.spineSegment, idx < step && styles.active)} />
            )}
          </div>
        )
      })}
    </div>
  )
}