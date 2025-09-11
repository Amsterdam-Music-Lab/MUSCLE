import type { Meta, StoryObj } from "@storybook/react";
import Spectrum from "./Spectrum";

type Story = StoryObj<typeof Spectrum>;

const decorator = (Story: Story) => (
  <div style={{ height: "200px" }}>
    <Story />
  </div>
);

const meta: Meta<typeof Spectrum> = {
  title: "Modules/Spectrum",
  component: Spectrum,
  decorators: [decorator],
};
export default meta;

export const Default: Story = {
  args: { running: true },
};

export const Random: Story = {
  args: {
    bars: 7,
    running: true,
    random: true,
    interval: 200,
  },
};

export const Slow: Story = {
  args: {
    ...Random.args,
    interval: 2000,
  },
};
