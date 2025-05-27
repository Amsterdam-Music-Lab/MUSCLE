/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import ExplainerView from "./ExplainerView";

export default {
  title: "Views/ExplainerView",
  component: ExplainerView,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

export const Default = {
  args: {
    instruction: "This is the instruction",
    button_label: "Next",
    steps: [
      { number: 1, description: "This is the first step" },
      { number: 2, description: "This is the second step" },
      { number: 3, description: "This is the third step" },
    ],
    onNext: () => {
      console.log("Next button clicked");
    },
    timer: null,
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};

export const WithOnClick = {
  args: {
    instruction: "This is the instruction",
    button_label: "Next",
    steps: [
      { number: 1, description: "This is the first step" },
      { number: 2, description: "This is the second step" },
      { number: 3, description: "This is the third step" },
    ],
    onNext: () => alert("Next button clicked"),
    timer: null,
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};

export const WithThreeSecondTimer = {
  args: {
    instruction: "This is the instruction",
    button_label: "Next",
    steps: [
      { number: 1, description: "This is the first step" },
      { number: 2, description: "This is the second step" },
      { number: 3, description: "This is the third step" },
    ],
    onNext: () => alert("Next button clicked / timer expired after 3 seconds"),
    timer: 3000,
  },
  decorators: [
    (Story) => (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#ddd",
          padding: "1rem",
        }}
      >
        <Story />
      </div>
    ),
  ],
};
