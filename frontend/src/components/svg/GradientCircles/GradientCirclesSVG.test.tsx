/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, expect, it } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import GradientCirclesSVG from "./GradientCirclesSVG";

describe("GradientCirclesSVG", () => {
  it("renders with default values", () => {
    const { container } = render(<GradientCirclesSVG />);
    const svg = container.querySelector("svg");
    const gradient = container.querySelector("linearGradient");
    const circles = container.querySelectorAll("circle");

    expect(svg).toBeTruthy();
    expect(gradient).toBeTruthy();
    expect(circles.length).toBe(12); // default numCircles
  });

  it("renders the correct number of circles", () => {
    const { container } = render(<GradientCirclesSVG numCircles={5} />);
    const circles = container.querySelectorAll("circle");
    expect(circles.length).toBe(5);
  });

  it("disables animation if animate=false", () => {
    const { container } = render(<GradientCirclesSVG animate={false} />);
    const animated = Array.from(container.querySelectorAll("circle")).filter(
      (c) => c.getAttribute("class")?.includes("animate")
    );

    expect(animated.length).toBe(0);
  });

  it("respects aspect ratio and height", () => {
    const height = 300;
    const aspect = 2;

    const { container } = render(
      <GradientCirclesSVG height={height} aspect={aspect} />
    );

    const svg = container.querySelector("svg");
    expect(svg?.getAttribute("viewBox")).toBe(
      `0 0 ${height * aspect} ${height}`
    );
  });

  it("renders a clipPath and applies it", () => {
    const { container } = render(<GradientCirclesSVG />);
    const clipPath = container.querySelector("clipPath");
    const group = container.querySelector("g");

    expect(clipPath).toBeTruthy();
    expect(group?.getAttribute("clip-path")).toMatch(/^url\(#clip-path-/);
  });
});
