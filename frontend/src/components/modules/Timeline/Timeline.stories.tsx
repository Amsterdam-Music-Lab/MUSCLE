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

export default {
  title: "Modules/Timeline",
  component: Timeline,
};

export const Default = {
  args: {
    timeline: timeline,
    step: 4,
  },
};

export const Alternative = {
  args: {
    timeline: timeline2,
    step: 7,
  },
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
};

export const NoSymbols = {
  args: {
    timeline: timeline,
    step: 5,
    showSymbols: false,
  },
};

export const NoSpine = {
  args: {
    timeline: timeline,
    step: 5,
    showSpine: false,
  },
};

export const NoDots = {
  args: {
    timeline: { ...timeline, showDots: false },
    step: 5,
  },
};

export const NoVariant = {
  args: {
    timeline: timeline2,
    step: 7,
    variant: null,
  },
};

export const PrimaryVariant = {
  args: {
    timeline: timeline2,
    step: 7,
    variant: "primary",
  },
};

export const SecondaryVariant = {
  args: {
    timeline: timeline2,
    step: 7,
    variant: "secondary",
  },
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
};
