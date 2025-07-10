/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { NarrowLayout } from "components/layout";
import ExplainerView from "./ExplainerView";

export default {
  title: "App/Views/ExplainerView",
  component: ExplainerView,
  decorators: [
    (Story) => (
      <NarrowLayout>
        <Story />
      </NarrowLayout>
    ),
  ],
  parameters: {
    backgrounds: {
      values: [{ value: "#ddd" }],
    },
  },
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
    onNext: () => alert("Next button clicked"),
  },
};

export const WithTimer = {
  args: {
    ...Default.args,
    onNext: () => alert("Timer expired after 500ms"),
    timer: 500,
  },
};
