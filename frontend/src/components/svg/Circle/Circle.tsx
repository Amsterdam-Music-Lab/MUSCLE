
interface CircleProps {
    cx: number;
    cy: number;
    r: number;
    fill: string;
    rotate: number;
    dur: number;
    animate: boolean;
}

export default function Circle({
  cx,
  cy,
  r,
  fill,
  rotate,
  dur,
  animate = true,
  ...props
}: CircleProps) {
  const styles = {}
  return (
    <circle
      cx={cx}
      cy={cy}
      r={r}
      fill={fill}
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