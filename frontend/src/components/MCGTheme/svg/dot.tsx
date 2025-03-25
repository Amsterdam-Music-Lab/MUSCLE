import "react"
import { colors } from "../colors";
import { SVGGradient, gradientId } from "./gradient";

interface SVGDotProps {
  size?: number;
  fill?: string;
  fillFrom?: string;
  fillTo?: string;
  animate?: boolean;
  className?: string;
}

export const SVGDot = ({
  size = 20,
  fill = undefined,
  fillFrom = colors['red'],
  fillTo = colors['pink'],
  animate = false,
  className = undefined
}: SVGDotProps) => {
  const id = gradientId()
  if (fill === undefined) {
    fill = `url(#${id})`
  }
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ top: `-${size / 2}px` }} className={className}>
      <circle cx={size / 2} cy={size / 2} r={(size - 1) / 2} fill={fill} className={ animate && "animate-rotate"} />
      <defs>
        <SVGGradient id={id} from={fillFrom} to={fillTo} />
      </defs>
    </svg>
  );
}