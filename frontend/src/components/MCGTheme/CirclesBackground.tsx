import * as React from "react";
import { colors } from "./colors";
import { type Color } from "./types";

interface SVGGradientProps {
    from: Color;
    to: Color;
    offset?: number;
    gradientUnits?: string;
}

export function SVGGradient({ from, to, offset = 0.4, gradentUnits='objectBoundingBox' }: SVGGradientProps) {
  return (
    <linearGradient
      id={`gradient-${from}-${to}`}
      x1={-1 * offset}
      y1="0"
      x2={1 + offset}
      y2="0"
      gradientUnits={gradentUnits}
      
    >
      <stop stopColor={colors[from]} />
      <stop offset="1" stopColor={colors[to]} />
    </linearGradient>
  );
}

interface CircleProps {
    cx: number;
    cy: number;
    r: number;
    rotate: number;
    from: string;
    to: string;
    dur: number;
    animate: boolean;
}

function Circle({
  cx,
  cy,
  r,
  rotate,
  from,
  to,
  dur,
  animate = true,
  ...props
}: CircleProps) {
  const styles = {}
  if(animate) {
    styles['animation'] = "rotate 2s infinite";
    styles['transformOrigin'] = `${cx} ${cy}`;
  }
  return (
    <circle
      cx={cx}
      cy={cy}
      r={r}
      fill={`url(#gradient-${from}-${to})`}
      className="gradient-circle"
      {...props}
    >
      {!dur || !animate ? null : (
        <animateTransform
          attributeName="transform"
          attributeType="XML"
          type="rotate"
          from={`0 ${cx} ${cy}`}
          to={`${Math.random() < 0.5 ? 360 : -360} ${cx} ${cy}`}
          dur={`${dur}s`}
          repeatCount="indefinite"
        />
      )}
    </circle>
  );
}

interface RandomCirclesProps {
    color1: color;
    color2: color;
    aspect?: number;
    numCircles?: number;
    gradientOffset?: number;
    animate?: boolean
}

function RandomCircles({
  color1 = "indigo",
  color2 = "red",
  aspect = 1,
  numCircles = 12,
  gradientOffset = 0.35,
  animate = true
}: RandomCirclesProps) {
  const height = 2000;
  const width = height * aspect;
  const minRadius = width / 20;

  const circleData = Array.from({ length: numCircles })
    .map(() => ({
      cx: Math.random() * width,
      cy: Math.random() * height,
      r: minRadius + Math.pow(10, 1 + 3 * Math.random()),
      rotate: Math.random() * 360,
      dur: 5 + Math.random() * 5,
      from: color1,
      to: color2,
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
          fill={`url(#gradient-${color1}-${color2})`}
        />
        {circleData.map((circle, i) => (
          <Circle key={i} {...circle} />
        ))}
      </g>

      <defs>
        <SVGGradient from={color1} to={color2} offset={gradientOffset} />
        <clipPath id="clip-path">
          <rect width={width} height={height} fill={colors.indigo} />
        </clipPath>
      </defs>
    </svg>
  );
}

interface CircleBackgroundProps {
    blur: number;
    color1: color;
    color2: color;
    animate?: boolean;
    numCircles: number;
}

export default function CirclesBackground({
  blur = 0,
  color1 = "indigo",
  color2 = "red",
  animate = true,
  numCircles = 12
} : CircleBackgroundProps) {
  return (
    <div className="circles-background position-static">
      <div
        className="position-absolute overflow-hidden w-100 h-100"
        style={{ zIndex: -2 }}
      >
        <RandomCircles color1={color1} color2={color2} animate={animate} numCircles={numCircles} />
      </div>
      {blur === 0 ? null : (
        <div
          className="position-absolute w-100"
          style={{
            backdropFilter: `blur(${blur}px)`,
            zIndex: -1,
            height: "200%",
          }}
        ></div>
      )}
    </div>
  );
}