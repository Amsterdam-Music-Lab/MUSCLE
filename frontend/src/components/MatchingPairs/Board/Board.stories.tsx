/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 * 
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import Board from "./Board";
import Card from "../Card/Card";

export default {
    title: "Matching Pairs/Board",
    component: Board,
    parameters: {
        layout: "fullscreen",
    },
    tags: ["autodocs"],
};

const decorator = (Story) => (
    <div style={{ padding: "1rem", }}>
        <Story />
    </div>
)

const divStyles = {
  textAlign:"center", 
  display: "flex",
  justifyContent: "center",
  flexDirection: "column",
  color: "#666"
}

function getDivs(num: number = 16) {
  return Array(num).fill(1).map((_, i) => 
    <div key={i} style={divStyles}>{i + 1}</div>
  )
}

export const Default = {
    args: {
      children: getDivs(),
    },
    decorators: [decorator]
};


export const ThreeColumns = {
  args: {
    children: getDivs(9),
    columns: 3,
  },
  decorators: [decorator]
};


export const OverflowColumns = {
  args: {
    children: getDivs(7),
    columns: 2,
  },
  decorators: [decorator]
};

function getCards(num: number = 16) {
  return Array(num).fill(1).map((_, i) => 
    <Card key={i} style={divStyles} />
  )
}

export const BoardOfCards = {
  args: {
    children: getCards(9),
    columns: 3,
  },
  decorators: [decorator]
}