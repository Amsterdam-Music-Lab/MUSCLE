import Star from "./Star";

export default {
  title: "Design System/SVG/Star",
  component: Star,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const decorator = (Story) => (
  <div style={{ padding: "1rem", background: "#f5f5f5" }}>
    <Story />
  </div>
);

export const Default = {
  args: {
    size: 100,
  },
  decorators: [decorator],
};

export const ManyPoints = {
  args: {
    size: 100,
    numPoints: 8,
    fill: "red",
  },
  decorators: [decorator],
};

export const LowSharpness = {
  args: {
    size: 100,
    sharpness: 0.3,
    fill: { startColor: "#ff0000", endColor: "#0000ff" },
  },
  decorators: [decorator],
};

export const StarSize = {
  args: {
    size: 100,
    starSize: 0.5,
    fill: { startColor: "#ff0000", endColor: "#0000ff" },
  },
  decorators: [decorator],
};

export const NoCircle = {
  args: {
    size: 100,
    showCircle: false,
    starFill: { startColor: "#ff0000", endColor: "#0000ff", angle: 90 },
  },
  decorators: [decorator],
};

export const Green = {
  args: {
    size: 100,
    fill: "#008800",
  },
  decorators: [decorator],
};

export const GreenGradientYellowStroke = {
  args: {
    size: 100,
    fill: { startColor: "#006600", endColor: "#00dd00" },
    starFill: { startColor: "#999900", endColor: "#ffff00" },
    circleStroke: "#ffff00cc",
    circleStrokeWidth: 0.15,
  },
  decorators: [decorator],
};

export const PrimaryVariant = {
  args: {
    size: 100,
    variant: "primary",
  },
  decorators: [decorator],
};

export const SecondaryVariant = {
  args: {
    size: 100,
    variant: "secondary",
  },
  decorators: [decorator],
};
