/**
 * author: Bas Cornelissen
 */
import { colors } from "./colors";
import { SVGStar } from "./svg/star";
import { SVGDot } from "./svg/dot";
import "./Timeline.scss";

type TimelineSymbolName = 'dot' | 'star' | 'star-4' | 'star-5' | 'star-6' | 'star-7';

export const TIMELINE_SYMBOLS = {
  'dot': ({ ...props }) => <SVGDot {...props} />,
  'star': ({ ...props }) => <SVGStar numPoints={5} {...props} />,
  'star-4': ({ ...props }) => <SVGStar numPoints={4} {...props} />,
  'star-5': ({ ...props }) => <SVGStar numPoints={5} {...props} />,
  'star-6': ({ ...props }) => <SVGStar numPoints={6} {...props} />,
  'star-7': ({ ...props }) => <SVGStar numPoints={7} {...props} />,
  'star-8': ({ ...props }) => <SVGStar numPoints={8} {...props} />
}

export type TimelineConfig = {
  symbol: TimelineSymbolName,
  size: number,
  animate: boolean,
  trophy: boolean
}

/**
 * Utility function that returns a timeline configuration object from a
 * sequence of timeline symbols. 
 * 
 * @param symbols A list of symbol names
 * @param dotSize The size of the dot
 * @param trophySize The size of a trophy symbol. Defaults to 3*dotSize
 * @param animate Animate the trophies?
 * @param showDots Show dots at all
 * @returns {TimelineConfig}
 */
export function getTimeline(
  symbols: Array[string],
  dotSize: number = 10,
  trophySize: number = null,
  animate: boolean = false,
  showDots: boolean = true,
): TimelineConfig {
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
  timeline: TimelineConfig;
  step: number;
  highlightColor?: string;
  mutedColor?: string;
  animate?: boolean;
  showSpine?: boolean;
  showSymbols?: boolean;
}

const Timeline = ({
  timeline,
  step = 0,
  highlightColor = undefined,
  mutedColor = '#eee',
  animate = true,
  showSpine = true,
  showSymbols = true,
}: TimelineProps) => {
  const steps = timeline.length;
  return (
    <div className="mcg-timeline position-relative" style={{ "--steps": steps }}>
      {showSymbols && (
        <div className="symbols d-flex justify-content-between">
          {timeline.map((symbol, idx) => {
            const Symbol = TIMELINE_SYMBOLS[symbol.symbol] || null;
            return (
              <div className="symbol" key={idx}>
                {Symbol && (
                  <div className="svg-wrapper">
                    <Symbol
                      size={symbol.size}
                      fill={idx < step ? highlightColor : mutedColor}
                      animate={animate && symbol.animate}
                      className="position-relative"
                      style={{ top: `-${symbol.size / 2}px` }}
                    />
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}

      {showSpine && <div className="spine">
        <div className="spine-bg" />
        <div
          className="spine-progress bg-red-pink"
          style={{ width: `${Math.floor((step - 1) / (steps - 1) * 100)}%` }}
        />
      </div>}
    </div>
  )
}

export default Timeline