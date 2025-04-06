/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import SVGStar from "@/components/SVG/SVGStar";
import SVGDot from "@/components/SVG/SVGDot";
import { SVGFill } from "../SVG/types";
import "./Timeline.scss";

type TimelineSymbolName = 'dot' | 'star' | 'star-4' | 'star-5' | 'star-6' | 'star-7' | null;

export const TIMELINE_SYMBOLS = {
  'dot': ({ ...props }) => <SVGDot {...props} />,
  'star': ({ ...props }) => <SVGStar numPoints={5} {...props} />,
  'star-4': ({ ...props }) => <SVGStar numPoints={4} {...props} />,
  'star-5': ({ ...props }) => <SVGStar numPoints={5} {...props} />,
  'star-6': ({ ...props }) => <SVGStar numPoints={6} {...props} />,
  'star-7': ({ ...props }) => <SVGStar numPoints={7} {...props} />,
  'star-8': ({ ...props }) => <SVGStar numPoints={8} {...props} />
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
  fillPast?: SVGFill;
  
  /** Fill of the future steps: everything after the current step */
  fillFuture?: SVGFill;

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
}: TimelineProps) {  
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
    <div className="timeline" style={{
      '--spine-bg-past': spineBgPast, '--spine-bg-future': spineBgFuture
    }}>
      {timeline.map((symbol, idx) => {
        const Symbol = symbol.symbol ? TIMELINE_SYMBOLS[symbol.symbol] : null;
        return (
          <div className="step" key={idx}>
            {showSymbols && Symbol && (
              <div className="symbol">
                <Symbol
                  size={symbol.size}
                  fill={idx < step ? fillPast : fillFuture}
                  animate={animate && symbol.animate}
                  style={{ top: `-${symbol.size / 2}px` }}
                />
              </div>
            )}
            {showSpine && (
              <div className={`spine-segment ${idx < step && 'active'}`} />
            )}
          </div>
        )
      })}
    </div>
  )
}