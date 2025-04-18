/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import React, { Children } from "react";
import ExpandableButton from "./ExpandableButton";

export default {
  title: "UI/Expandable Button",
  component: ExpandableButton,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const decorator = (Story) => (
  <div
    style={{
      maxWidth: "400px",
      height: "100%",
      padding: "1rem",
    }}
  >
    <Story />
  </div>
);

const Options = ({ children }: { children: React.ReactNode }) => (
  <div
    style={{
      display: "flex",
      gap: ".75em",
    }}
  >
    {Children.toArray(children).map((child, i) => (
      <div
        key={i}
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          flexShrink: 0,
        }}
      >
        {child}
      </div>
    ))}
  </div>
);

export const Default = {
  args: {
    title: "Click me",
    children: (
      <Options>
        <span key="option1">Option 1 asdfasdf asdf</span>
        <span key="option2">Option 2</span>
        <span key="option3">Option 3</span>
      </Options>
    ),
    onClick: () => {
      console.log("Button clicked");
    },
  },
  decorators: [decorator],
};

export const WithText = {
  args: {
    title: "More",
    expanded: true,
    children: (
      <div style={{ display: "flex", flexShrink: 0 }}>
        <div>Lorem ipsum dolor sed amet</div>
      </div>
    ),
  },
  decorators: [decorator],
};

export const ButtonProps = {
  args: {
    title: "More",
    variant: "secondary",
    rounded: false,
    children: (
      <div style={{ display: "flex", flexShrink: 0 }}>
        <div>Lorem ipsum dolor sed amet</div>
      </div>
    ),
  },
  decorators: [decorator],
};

export const Disabled = {
  args: {
    title: "More",
    disabled: true,
    expanded: true,
    children: "Hallo!",
  },
  decorators: [decorator],
};
