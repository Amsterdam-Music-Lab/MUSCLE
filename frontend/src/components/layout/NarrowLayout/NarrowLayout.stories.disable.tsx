/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import NarrowLayout from "./NarrowLayout";

const decorator = (Story: () => JSX.Element) => (
  <div
    style={{
      padding: "1rem",
    }}
  >
    <Story />
  </div>
);

const meta =  {
  title: "NarrowLayout",
  component: NarrowLayout,
  parameters: {
    layout: "fullscreen",
  },
  decorators: [decorator],
  tags: ["autodocs"],
};

export default meta

export const Default = {
  args: {},
};
