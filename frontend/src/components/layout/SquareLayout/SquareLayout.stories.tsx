/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { useOrientation } from "@/hooks/OrientationProvider";
import SquareLayout from "./SquareLayout";

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
  title: "Game UI/SquareLayout",
  component: SquareLayout,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
};

export const Landscape = {
  args: {
    debug: true,
    children: [
      <SquareLayout.Header>Header</SquareLayout.Header>,
      <SquareLayout.Square>Main</SquareLayout.Square>,
      <SquareLayout.Aside>Aside</SquareLayout.Aside>,
      <SquareLayout.Footer>Footer</SquareLayout.Footer>,
    ],
  },
  decorators: [getDecorator("600px", "300px")],
};

export const Portrait = {
  args: {
    debug: true,
    children: [
      <SquareLayout.Header>Header</SquareLayout.Header>,
      <SquareLayout.Square>Main</SquareLayout.Square>,
      <SquareLayout.Aside>Aside</SquareLayout.Aside>,
      <SquareLayout.Footer>Footer</SquareLayout.Footer>,
    ],
  },
  decorators: [getDecorator("300px", "600px")],
};

export const Responsive = {
  args: {
    debug: true,
    children: [
      <SquareLayout.Header>Header</SquareLayout.Header>,
      <SquareLayout.Square>Main</SquareLayout.Square>,
      <SquareLayout.Aside>Aside</SquareLayout.Aside>,
      <SquareLayout.Footer>Footer</SquareLayout.Footer>,
    ],
  },
  decorators: [getDecorator("100vw", "100vh")],
};

export const ResponsiveNoAside = {
  args: {
    debug: true,
    children: [
      <SquareLayout.Header>Header</SquareLayout.Header>,
      <SquareLayout.Square>Main</SquareLayout.Square>,
      <SquareLayout.Footer>Footer</SquareLayout.Footer>,
    ],
  },
  decorators: [getDecorator("100vw", "100vh")],
};

const TestComponent = () => {
  const orientation = useOrientation();
  return <div>{orientation}</div>;
};

export const UseOrientation = {
  args: {
    debug: true,
    children: [
      <SquareLayout.Square>
        <TestComponent />
      </SquareLayout.Square>,
    ],
  },
  decorators: [getDecorator("100vw", "100vh")],
};
