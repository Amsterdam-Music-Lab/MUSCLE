
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