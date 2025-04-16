/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import type { ReactNode, CSSProperties, HTMLAttributes } from "react";

import type { Decorator } from "@storybook/react";
import Board from "./Board";
import { getDivs, getColoredSlots } from "./utils";
import Card from "../Card/Card";

const divStyles = {
  textAlign: "center",
  display: "flex",
  justifyContent: "center",
  flexDirection: "column",
  color: "#666",
} as CSSProperties;

export default {
  title: "Matching Pairs/Board",
  component: Board,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

const decorator: Decorator = (Story) => (
  <div style={{ padding: "1rem" }}>
    <Story />
  </div>
);

export const Default = {
  args: {
    children: getDivs(16, { style: divStyles }),
  },
  decorators: [decorator],
};

export const ThreeColumns = {
  args: {
    children: getDivs(9, { style: divStyles }),
    columns: 3,
  },
  decorators: [decorator],
};

export const OverflowColumns = {
  args: {
    children: getDivs(7, { style: divStyles }),
    columns: 2,
  },
  decorators: [decorator],
};

function getCards(num: number = 16) {
  return Array(num)
    .fill(1)
    .map((_, i) => <Card key={i} style={divStyles} />);
}

export const BoardOfCards = {
  args: {
    children: getCards(9),
    columns: 3,
  },
  decorators: [decorator],
};

export const StyleSlots = {
  args: {
    columns: 3,

    // Note that you need to use items instead of children
    // because Storybook won't accept objects as children (!?)
    items: getColoredSlots(9, { style: divStyles }),
  },
  decorators: [decorator],
};

export const InvisibleSlots = {
  args: {
    columns: 3,

    // Note that you need to use items instead of children
    // because Storybook won't accept objects as children (!?)
    items: getDivs(9, { style: divStyles }).map((card, index) => [
      card,
      { invisible: index % 2 === 0 },
    ]),
  },
  decorators: [decorator],
};
