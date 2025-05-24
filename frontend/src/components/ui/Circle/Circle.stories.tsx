import Circle from "./Circle";

const decoratorStyles = {
  width: "100%",
  height: "100%",
  backgroundColor: "#666",
  padding: "1rem",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

const decorator = (Story) => (
  <div style={decoratorStyles}>
    <Story />
  </div>
);

export default {
  title: "UI/Circle",
  component: Circle,
  decorators: [decorator],
};

export const Default = {
  args: {},
};

export const NoAnimation = {
  args: {
    ...Default.args,
    animateCircle: false,
  },
};

export const NoRunning = {
  args: {
    ...Default.args,
    animateCircle: true,
    running: false,
  },
};

export const NoAnimationNoRunning = {
  args: {
    ...Default.args,
    animateCircle: false,
    running: false,
  },
};

export const ShortDuration = {
  args: {
    ...Default.args,
    duration: 1,
    animateCircle: true,
    running: true,
  },
};

export const LongDuration = {
  args: {
    ...Default.args,
    duration: 60,
    animateCircle: true,
    running: true,
  },
};

export const NoDuration = {
  args: {
    radius: 100,
    strokeWidth: 5,
    color: "white",
    duration: 0,
    animateCircle: true,
    running: true,
  },
};

export const ThickStroke = {
  args: {
    ...Default.args,
    strokeWidth: 20,
  },
};

export const OnTickOnFinish = {
  args: {
    ...Default.args,
    duration: 2,
    onTick: (t) => console.log("Tick", t),
    onFinish: () => console.log("Finished"),
  },
  decorators: [
    (Story) => (
      <div style={decoratorStyles}>
        <p>Check the console</p>
        <Story />
      </div>
    ),
  ],
};

export const Children = {
  args: {
    ...Default.args,
    children: <span>Test</span>,
  },
};

export const InfiniteRotation = {
  args: {
    ...Children.args,
    start: 50,
    duration: 2,
    running: false,
    startTime: 0.2,
    rotate: true,
  },
};
