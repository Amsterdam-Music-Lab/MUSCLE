import Timeline from "./Timeline";

const timeline = {
  symbols: [
    "dot",
    "dot",
    "star-4",
    "dot",
    "dot",
    "star-5",
    "dot",
    "dot",
    "star-6",
  ],
};

const timeline2 = {
  symbols: [
    "star-5",
    "dot",
    "star-4",
    "dot",
    "dot",
    "star-7",
    "dot",
    "dot",
    "dot",
    "star-8",
  ],
};

const decorator = (Story) => (
  <div style={{ padding: "1rem", background: "#f5f5f5" }}>
    <Story />
  </div>
);

export default {
  title: "Modules/Timeline",
  component: Timeline,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

export const Default = {
  args: {
    timeline: timeline,
    step: 4,
  },
  decorators: [decorator],
};

export const Alternative = {
  args: {
    timeline: timeline2,
    step: 7,
  },
  decorators: [decorator],
};

export const CustomFill = {
  args: {
    timeline: timeline,
    step: 4,
    fillPast: {
      startColor: "#ff0000",
      endColor: "#00ff00",
      scale: 2,
      angle: 60,
    },
  },
  decorators: [decorator],
};

export const NoSymbols = {
  args: {
    timeline: timeline,
    step: 5,
    showSymbols: false,
  },
  decorators: [decorator],
};

export const NoSpine = {
  args: {
    timeline: timeline,
    step: 5,
    showSpine: false,
  },
  decorators: [decorator],
};

export const NoDots = {
  args: {
    timeline: { ...timeline, showDots: false },
    step: 5,
  },
  decorators: [decorator],
};

export const NoVariant = {
  args: {
    timeline: timeline2,
    step: 7,
    variant: null,
  },
  decorators: [decorator],
};

export const PrimaryVariant = {
  args: {
    timeline: timeline2,
    step: 7,
    variant: "primary",
  },
  decorators: [decorator],
};

export const SecondaryVariant = {
  args: {
    timeline: timeline2,
    step: 7,
    variant: "secondary",
  },
  decorators: [decorator],
};

export const CustomizeEverything = {
  args: {
    timeline: {
      steps: [
        { symbol: "dot" },
        { symbol: "star-4", fill: "#0ff" },
        { symbol: "star-5", fill: "#f00", size: 80 },
        { symbol: "star-6", size: 50, fill: "#ff0" },
      ],
      // variant: "secondary",
      fill: "#0f0",
    },
    step: 3,
  },
  decorators: [decorator],
};
