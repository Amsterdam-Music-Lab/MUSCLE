import "react";

interface SVGGradientProps {
  id: string;
  from: string;
  to: string;
  x1?: number;
  y1?: number;
  x2?: number;
  y2?: number;
  gradientUnits?: string;
}

export const SVGGradient = ({
  id,
  from,
  to,
  x1 = 0,
  y1 = 0,
  x2 = 1,
  y2 = 1,
  gradientUnits = 'objectBoundingBox'
}: SVGGradientProps) => {
  return (
    <linearGradient
      id={id}
      x1={x1}
      y1={y1}
      x2={x2}
      y2={y2}
      gradientUnits={gradientUnits}
    >
      <stop stopColor={from} />
      <stop offset="1" stopColor={to} />
    </linearGradient>
  );
}

export function gradientId() {
  return `gradient-${Math.random().toString(16).slice(2)}`
}