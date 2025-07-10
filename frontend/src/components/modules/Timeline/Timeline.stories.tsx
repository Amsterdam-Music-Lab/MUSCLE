import Timeline from "./Timeline";

const timeline = {
  currentStep: 4,
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
  currentStep: 7,
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

export default {
  title: "Modules/Timeline",
  component: Timeline,
};

export const Default = {
  args: {
    timeline: timeline,
  },
};

export const Alternative = {
  args: {
    timeline: timeline2,
  },
};

export const CustomFill = {
  args: {
    timeline: timeline,
    fillPast: {
      startColor: "#ff0000",
      endColor: "#00ff00",
      scale: 2,
      angle: 60,
    },
  },
};

export const NoSymbols = {
  args: {
    timeline: timeline,
    showSymbols: false,
  },
};

export const NoSpine = {
  args: {
    timeline: timeline,
    showSpine: false,
  },
};

export const NoDots = {
  args: {
    timeline: { ...timeline, showDots: false },
  },
};

export const PrimaryVariant = {
  args: {
    timeline: timeline2,
    variant: "primary",
  },
};

export const SecondaryVariant = {
  args: {
    timeline: timeline2,
    variant: "secondary",
  },
};

export const CustomizeEverything = {
  args: {
    timeline: {
      currentStep: 3,
      steps: [
        { symbol: "dot" },
        { symbol: "star-4", fill: "#0ff" },
        { symbol: "star-5", fill: "#f00", size: 80 },
        { symbol: "star-6", size: 50, fill: "#ff0" },
      ],
      fill: "#0f0",
    },
  },
};
