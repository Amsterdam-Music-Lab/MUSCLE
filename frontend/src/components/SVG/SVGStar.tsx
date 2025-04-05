import "react"
import { colors } from "../MCGTheme/colors"; // TODO remove this
import { SVGGradient, gradientId } from "./SVGGradient";

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
  fillFrom?: string,
  fillTo?: string,
  animate?: boolean;
  className?: string;
  strokeWidthFactor?: number;
}

export const SVGStar = ({
  numPoints = 5,
  sharpness = .6,
  size = 20,
  fill = undefined,
  fillFrom = colors['red'],
  fillTo = colors['pink'],
  animate = true,
  className = undefined,
  strokeWidthFactor = 0.2,
  ...props // we only need style, reallly, but still
}: SVGStarProps) => {
  // Use a gradient fill by default
  const id = gradientId()
  if (fill === undefined) {
    fill = `url(#${id})`
  }

  const center = size / 2; // Center the star
  const strokeWidth = strokeWidthFactor * size
  const outerRadius = (size * .7) / 2; // Maximum radius is half the size
  const innerRadius = (1 - sharpness) * outerRadius; // Scale inner radius
  const pathData = createStarPath(center, center, numPoints, innerRadius, outerRadius);

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      className={className}
      {...props}
    >
      <g className={animate ? "animate-rotate" : ""}>
        <circle
          cx={size / 2} cy={size / 2} r={(size - 1) / 2}
          fill={fill}
          strokeWidth={strokeWidth}
          stroke="#ffffff33"
        />
        <path d={pathData} fill="white" />
      </g>
      <defs>
        <SVGGradient id={id} from={fillFrom} to={fillTo} />
      </defs>
    </svg>
  );
};