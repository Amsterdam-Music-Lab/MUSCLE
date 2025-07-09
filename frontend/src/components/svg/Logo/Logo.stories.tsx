/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Logo from "./Logo";

const decorator = (Story: () => JSX.Element) => (
  <div
    style={{
      padding: "1rem",
      width: "200px",
      border: "1px dotted black",
    }}
  >
    <Story />
  </div>
);

export default {
  title: "Design System/SVG/Logo",
  component: Logo,
  parameters: {
    layout: "fullscreen",
  },
  decorators: [decorator],
  tags: ["autodocs"],
};

export const TuneTwins = {
  args: {
    name: "tunetwins",
  },
};

export const Fill = {
  args: {
    name: "tunetwins",
    fill: "red",
  },
};

export const Variants = {
  args: {
    name: "tunetwins",
    variant: "secondary",
  },
};

export const AML = {
  args: {
    name: "aml",
  },
};

export const AMLWordmark = {
  args: {
    name: "aml",
    type: "lockup",
    // knockout: true,
  },
};

export const MCG = {
  args: {
    name: "mcg",
  },
};

export const MCGKnockout = {
  args: {
    name: "mcg",
    knockout: true,
  },
};

export const MCGLockup = {
  args: {
    name: "mcg",
    type: "lockup",
  },
};

export const MCGLockupKnockout = {
  args: {
    name: "mcg",
    type: "lockup",
    knockout: true,
    fill: "#999",
  },
};

export const Uva = {
  args: {
    name: "uva",
    fill: "#000",
  },
};

export const UvaKnockout = {
  args: {
    name: "uva",
    fill: "green",
    knockout: true,
  },
};

export const UvaLockup = {
  args: {
    name: "uva",
    type: "lockup",
  },
};

export const NWO = {
  args: {
    name: "nwo",
  },
};
