/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import Button from "./Button";

export default {
  title: "UI/Button",
  component: Button,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const decorator = (Story) => (
  <div
    style={{
      maxWidth: "300px",
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

export const Stretch = {
  args: {
    title: "Stretched link",
    stretch: true,
  },
  decorators: [decorator],
};

export const Small = {
  args: {
    title: "Small button",
    size: "sm",
  },
  decorators: [decorator],
};

export const Medium = {
  args: {
    title: "Medium",
    size: "md",
  },
  decorators: [decorator],
};

export const Large = {
  args: {
    title: "Large",
    size: "lg",
  },
  decorators: [decorator],
};

export const NoOutline = {
  args: {
    title: "Large",
    size: "lg",
    outline: false,
  },
  decorators: [decorator],
};

export const Disabled = {
  args: {
    title: "Click me",
    disabled: true,
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
