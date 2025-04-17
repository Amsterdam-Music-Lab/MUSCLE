import { Button } from "@/components/ui";

export default {
  title: "UI/Button",
  component: Button,
  parameters: {
    layout: "fullscreen",
  },
};

const decorator = (Story) => (
  <div
    style={{
      maxWidth: "200px",
      height: "100%",
      padding: "1rem",
      background: "#eee",
    }}
  >
    <Story />
  </div>
);

export const Default = {
  args: {
    title: "Click me",
    onClick: () => {},
  },
  decorators: [decorator],
};

export const VeryLong = {
  args: {
    title: "Lorem ipsum dolor sed amet lorem ipsum dolor sed amet",
    onClick: () => {},
  },
  decorators: [decorator],
};

export const Inactive = {
  args: {
    title: "Click me",
    onClick: () => {},
  },
  decorators: [decorator],
};

export const WithValue = {
  args: {
    title: "Click me",
    onClick: () => {},
    value: "value",
  },
  decorators: [decorator],
};

export const Primary = {
  args: {
    title: "Click me",
    onClick: () => {},
    className: "btn-primary",
  },
  decorators: [decorator],
};

export const Secondary = {
  args: {
    title: "Click me",
    onClick: () => {},
    variant: "secondary",
  },
  decorators: [decorator],
};

export const Success = {
  args: {
    title: "Click me",
    onClick: () => {},
    variant: "success",
  },
  decorators: [decorator],
};

export const Danger = {
  args: {
    title: "Click me",
    onClick: () => {},
    variant: "danger",
  },
  decorators: [decorator],
};

export const Warning = {
  args: {
    title: "Click me",
    onClick: () => {},
    variant: "warning",
  },
  decorators: [decorator],
};

export const Info = {
  args: {
    title: "Click me",
    onClick: () => {},
    variant: "info",
  },
  decorators: [decorator],
};

export const WithOnClick = {
  args: {
    title: "Click me",
    onClick: () => alert("Clicked!"),
  },
  decorators: [decorator],
};
