/**
 * author: Bas Cornelissen
 */
import "react";


/*************************************
 ************** Symbols **************
 *************************************/


/**
 * Return the path string of an star with a given number of points and a 
 * given inner- and outer radius.
 * 
 * @param {number} cx 
 * @param {number} cy 
 * @param {number} numPoints 
 * @param {number} innerRadius 
 * @param {number} outerRadius 
 * @returns {str}
 */
const createStarPath = (
  cx: number,
  cy: number,
  numPoints: number,
  innerRadius: number,
  outerRadius: number
): string => {
  let path = "";
  const angle = (Math.PI * 2) / numPoints; // Angle between points

  for (let i = 0; i < numPoints * 2; i++) {
    const r = i % 2 === 0 ? outerRadius : innerRadius;
    const x = cx + r * Math.cos(i * angle / 2);
    const y = cy + r * Math.sin(i * angle / 2);
    path += i === 0 ? `M ${x},${y}` : ` L ${x},${y}`;
  }

  return path + " Z"; // Close the path
};

interface SVGStarProps {
  numPoints?: number;
  sharpness?: number;
  size?: number;
  fill?: string;
  className?: string;
}

const SVGStar = ({ 
  numPoints = 5, 
  sharpness = .6, 
  size = 20, 
  fill = 'black', 
  className = undefined 
}: SVGStarProps) => {
  const center = size / 2; // Center the star
  const outerRadius = size / 2; // Maximum radius is half the size
  const innerRadius = (1 - sharpness) * outerRadius; // Scale inner radius
  const pathData = createStarPath(center, center, numPoints, innerRadius, outerRadius);

  return (
    <svg 
      width={size} 
      height={size} 
      viewBox={`0 0 ${size} ${size}`} 
      className={className}
      style={{ top: `-${size / 2}px` }}
    >
      <path d={pathData} fill={fill} />
    </svg>
  );
};

interface SVGDotProps {
  size?: number;
  fill?: string;
  className?: string;
}

const SVGDot = ({ 
  size = 20, 
  fill = 'black', 
  className = undefined 
}: SVGDotProps) => {
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ top: `-${size / 2}px` }} className={className}>
      <circle cx={size / 2} cy={size / 2} r={(size-1) / 2} fill={fill} />
    </svg>
  );
}

type TimelineSymbolName = 'dot' | 'star' | 'star-4' | 'star-5' | 'star-6' | 'star-7';

const SYMBOLS = {
  'dot': ({ ...props }) => <SVGDot {...props} />,
  'star': ({ ...props }) => <SVGStar numPoints={5} {...props} />,
  'star-4': ({ ...props }) => <SVGStar numPoints={4} {...props} />,
  'star-5': ({ ...props }) => <SVGStar numPoints={5} {...props} />,
  'star-6': ({ ...props }) => <SVGStar numPoints={6} {...props} />,
  'star-7': ({ ...props }) => <SVGStar numPoints={7} {...props} />
}


/*************************************
 ************** Timeline *************
 *************************************/


interface TimelineProps {
  step: number;
  numSteps?: number;
  symbol?: TimelineSymbolName;
  symbols?: Array<TimelineSymbolName>;
  highlightColor?: string;
  mutedColor?: string;
  wiggle?: boolean;
  turns?: number;
  directionUp?: boolean;
  minSize?: number;
  growFactor?: number;
}

/**
 * Renders a discrete timeline with variable symbols at every step. The symbols
 * can be specified as an arraw `symbols` of symbol names, or, when using identical 
 * symbols, by `numSteps` and `symbol`. The timeline is wiggly, but can be straightened
 * by setting `wiggly = false`. The number of turns (or waves) can be adjusted by setting
 * `turns`. 
 * 
 * The timeline uses flexbox to evenly spread out the symbols even if they have varying
 * sizes. The amplitude of the wiggle is set relative to the parent height (as a percentage).
 * Changing the parent height will automatically change the amplitude of the wiggle.
 * 
 * @param {number} step - Current step in the timeline, determining which symbols are highlighted.
 * @param {Array<string>|undefined} symbols - Array of symbol names to display; defaults to identical symbols.
 * @param {number} numSteps - Total number of steps in the timeline.
 * @param {string} symbol - Default symbol to use if `symbols` is not provided.
 * @param {string} highlightColor - Color for active (highlighted) symbols.
 * @param {string} mutedColor - Color for inactive (muted) symbols.
 * @param {boolean} wiggle - Whether symbols should have a wiggling effect.
 * @param {number} turns - Number of oscillations for the vertical positioning of symbols.
 * @param {boolean} directionUp - Whether the oscillation direction is upwards.
 * @param {number} minSize - Minimum size of the symbols.
 * @param {number} growFactor - Scaling factor for symbol growth across the timeline.
 * 
 * @returns {JSX.Element}
 */
const Timeline = ({
  step, 
  symbols = undefined,
  numSteps = 10,
  symbol = 'dot',
  highlightColor = 'black',
  mutedColor = '#eee',
  wiggle = false,
  turns = 3,
  directionUp = true,
  minSize = 7,
  growFactor = 2.5,
}: TimelineProps) => {

  // Default to a series of identical symbols
  if (!symbols) {
    symbols = Array(numSteps).fill(symbol)
  }
  return (
    <div className="timeline d-flex justify-content-around w-100 h-100 position-relative overflow-hidden">
      {symbols.map((name, idx) => {
        const Symbol = SYMBOLS[name];
        const color = idx < step ? highlightColor : mutedColor;
        
        // Size of the symbol
        const relIdx = idx / (symbols.length - 1);
        let size = minSize + relIdx * growFactor * minSize;
        if(name.startsWith('star')) size *= 2;

        // Vertical position, determined using a sine wave
        const dir = directionUp ? -1 : 1
        const offset = Math.sin(relIdx * turns * Math.PI);
        const yPos = 50 + dir * offset * 25;

        return (
          <div className="symbol position-relative" key={idx}>
            <div 
              className="position-relative d-flex" 
              style={wiggle ? {top: `${yPos}%`} : {top: "50%"}}
            >
              <Symbol size={size} fill={color} className="position-relative" />
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default Timeline