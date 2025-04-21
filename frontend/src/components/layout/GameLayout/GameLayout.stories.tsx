/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import GameLayout from "./GameLayout";

function getDecorator(width: string, height: string) {
  return (Story) => (
    <div
      style={{
        padding: "1rem",
        width,
        height,
      }}
    >
      <Story />
    </div>
  );
}

export default {
  title: "Game UI/GameLayout",
  component: GameLayout,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

export const Landscape = {
  args: {
    debug: true,
    children: [
      <GameLayout.Header>Header</GameLayout.Header>,
      <GameLayout.Main>Main</GameLayout.Main>,
      <GameLayout.FooterLeft>Footer Left</GameLayout.FooterLeft>,
      <GameLayout.FooterMain>Footer main</GameLayout.FooterMain>,
    ],
  },
  decorators: [getDecorator("600px", "300px")],
};

export const Portrait = {
  args: {
    debug: true,
    children: [
      <GameLayout.Header>Header</GameLayout.Header>,
      <GameLayout.Main>Main</GameLayout.Main>,
      <GameLayout.FooterLeft>Footer Left</GameLayout.FooterLeft>,
      <GameLayout.FooterMain>Footer main</GameLayout.FooterMain>,
    ],
  },
  decorators: [getDecorator("300px", "600px")],
};

export const Responsive = {
  args: {
    debug: true,
    children: [
      <GameLayout.Header>Header</GameLayout.Header>,
      <GameLayout.Main>Main</GameLayout.Main>,
      <GameLayout.FooterLeft>Footer Left</GameLayout.FooterLeft>,
      <GameLayout.FooterMain>Footer main</GameLayout.FooterMain>,
    ],
  },
  decorators: [getDecorator("100vw", "100vh")],
};
