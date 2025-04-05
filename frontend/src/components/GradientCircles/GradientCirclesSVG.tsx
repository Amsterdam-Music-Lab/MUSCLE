import * as React from "react";
import { gradientId, SVGGradient } from "../SVG/SVGGradient";
import { SVGCircle } from "../SVG/SVGCircle";

interface GradientCirclesSVGProps {
    color1: string;
    color2: string;
    aspect?: number;
    height?: number;
    numCircles?: number;
    gradientOffset?: number;
    animate?: boolean
    meanDuration?: number;
    minRadiusFactor?: number;
}

export default function GradientCirclesSVG({
  color1 = "#ff0000",
  color2 = "#00ff00",
  aspect = 1,
  height = 2000,
  numCircles = 12,
  gradientOffset = 0.35,
  animate = true,
  meanDuration = 5,
  minRadiusFactor = 0.2,
}: GradientCirclesSVGProps) {
  
  const width = height * aspect;
  const minRadius = minRadiusFactor * width;
  const id = gradientId()
  const circleData = Array.from({ length: numCircles })
    .map(() => ({
      cx: Math.random() * width,
      cy: Math.random() * height,
      r: minRadius + Math.pow(10, 1 + 3 * Math.random()),
      rotate: Math.random() * 360,
      dur: meanDuration + Math.random() * meanDuration,
      fill: `url(#${id})`,
      animate: animate
    }))
    .sort((a, b) => (a.r - b.r) * Math.random() < 0);

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ objectFit: "cover", minHeight: "100%", minWidth: "100%" }}
    >
      <g clipPath="url(#clip-path)">
        <rect
          width={width}
          height={height}
          fill={`url(#${id})`}
        />
        {circleData.map((circle, i) => (
          <SVGCircle key={i} {...circle} />
        ))}
      </g>

      <defs>
        <SVGGradient 
          id={id}
          from={color1} 
          to={color2} 
          x1={-1 * gradientOffset} 
          y1={0} 
          x2={1 + gradientOffset} 
          y2={0} />
        <clipPath id="clip-path">
          <rect width={width} height={height} fill={`url(#${id})`} />
        </clipPath>
      </defs>
    </svg>
  );
}
