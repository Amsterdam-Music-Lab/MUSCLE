import Timeline from "./Timeline";
import useBoundStore from "@/util/stores";

const timeline = {
  playedSessions: 4,
  steps: [
    {},
    {},
    {image: "star"},
    {},
    {},
    {image: "star"},
    {},
    {},
    {image: "cup"},
  ],
};

const timeline2 = {
  playedSessions: 7,
  steps: [
    {image: "star"},
    {},
    {image: "star"},
    {},
    {},
    {image: "star"},
    {},
    {},
    {},
    {image: "cup"},
  ],
};

const getDecorator = (Story) => {
    const setTheme = useBoundStore((state) => state.setTheme);
    setTheme({ colorPrimary: '#d843e2', colorGrey: '#bdbebf' });
    return (
      <div
          style={{ width: "100%", height: "100%", backgroundColor: "#9e9fa1", padding: "1rem" }}
      >
        <Story />
      </div>
    );
}

export default {
  title: "Timeline/Timeline",
  component: Timeline,
};

export const Default = {
  args: {
    timeline: timeline,
  },
  decorators: [getDecorator]
};

export const Alternative = {
  args: {
    timeline: timeline2,
  },
  decorators: [getDecorator]
};

export const CustomFill = {
  args: {
    timeline: timeline,
  },
  decorators: [getDecorator]
};

export const NoSymbols = {
  args: {
    timeline: timeline,
    showSymbols: false,
  },
  decorators: [getDecorator]
};

export const NoSpine = {
  args: {
    timeline: timeline,
    showSpine: false,
  },
  decorators: [getDecorator]
};

export const NoDots = {
  args: {
    timeline: { ...timeline, showDots: false },
  },
  decorators: [getDecorator]
};

export const PrimaryVariant = {
  args: {
    timeline: timeline2,
    variant: "primary",
  },
  decorators: [getDecorator]
};

export const SecondaryVariant = {
  args: {
    timeline: timeline2,
    variant: "secondary",
  },
  decorators: [getDecorator]
};

