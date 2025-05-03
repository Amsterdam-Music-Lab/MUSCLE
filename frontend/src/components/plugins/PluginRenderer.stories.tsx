import type { Meta, StoryObj } from "@storybook/react";
import PluginRenderer from "./PluginRenderer";

const meta: Meta<typeof PluginRenderer> = {
  component: PluginRenderer,
  title: "Plugins/PluginRenderer",
  args: {},
};

export default meta;

type Story = StoryObj<typeof PluginRenderer>;

export const Basic: Story = {
  args: {
    plugins: [
      { name: "logo", args: { name: "mcg" } },
      { name: "scores", args: { turnScore: 42 } },
    ],
  },
};

export const WithWrapper: Story = {
  args: {
    plugins: [
      {
        name: "logo",
        args: { name: "mcg" },
        getWrapperProps: (args) => ({ className: `logo-${args.name}` }),
      },
      { name: "logo", args: { name: "aml" } },
    ],
    wrapper: ({ children, className }) => (
      <div
        data-testid="wrapper"
        className={className}
        style={{ padding: ".5em", background: "#f5f5f5", margin: "1em" }}
      >
        {children}
      </div>
    ),
  },
};

export const WithSlots: Story = {
  args: {
    plugins: [
      { name: "logo", args: { name: "aml" }, slot: "header" },
      { name: "scores", args: { turnScore: 75 }, slot: "main" },
    ],
    renderSlot: (slot, children) => {
      switch (slot) {
        case "header":
          return <header key={slot}>HEADER {children}</header>;
        case "main":
          return <main key={slot}>MAIN {children}</main>;
        default:
          return <div key={slot}>REST {children}</div>;
      }
    },
  },
};

export const ConditionalVisibility: Story = {
  args: {
    plugins: [
      { name: "logo", args: { name: "mcg" }, enabled: true },
      { name: "logo", args: { name: "aml" }, isVisible: () => false },
    ],
  },
};
