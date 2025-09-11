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
import Gradient from "./Gradient";

describe("Gradient", () => {
  it("renders a linearGradient with correct id and default props", () => {
    const { container } = render(
      <Gradient id="test-gradient" startColor="#000" endColor="#fff" />
    );

    const gradient = container.querySelector("linearGradient");
    expect(gradient).toBeTruthy();
    expect(gradient).toHaveAttribute("id", "test-gradient");
    expect(gradient).toHaveAttribute("gradientUnits", "objectBoundingBox");

    const stops = container.querySelectorAll("stop");
    expect(stops.length).toBe(2);
    expect(stops[0]).toHaveAttribute("stop-color", "#000");
    expect(stops[1]).toHaveAttribute("stop-color", "#fff");
    expect(stops[1]).toHaveAttribute("offset", "1");
  });

  it("calculates x1/y1/x2/y2 based on angle and scale", () => {
    const { container } = render(
      <Gradient
        id="angle-test"
        startColor="red"
        endColor="blue"
        angle={90}
        scale={1}
      />
    );

    const grad = container.querySelector("linearGradient");
    const x1 = parseFloat(grad!.getAttribute("x1")!);
    const y1 = parseFloat(grad!.getAttribute("y1")!);
    const x2 = parseFloat(grad!.getAttribute("x2")!);
    const y2 = parseFloat(grad!.getAttribute("y2")!);

    // For angle 90°, x1 = x2 = 0.5, y1 = 0, y2 = 1
    expect(x1).toBeCloseTo(0.5, 5);
    expect(x2).toBeCloseTo(0.5, 5);
    expect(y1).toBeCloseTo(0, 5);
    expect(y2).toBeCloseTo(1, 5);
  });

  it("uses default colors when not provided", () => {
    const { container } = render(<Gradient id="fallback-test" />);
    const stops = container.querySelectorAll("stop");

    expect(stops[0]).toHaveAttribute("stop-color", "var(--start-color)");
    expect(stops[1]).toHaveAttribute("stop-color", "var(--end-color)");
  });

  it("passes through extra props like gradientTransform", () => {
    const { container } = render(
      <Gradient id="custom-transform" gradientTransform="rotate(45)" />
    );

    const gradient = container.querySelector("linearGradient");
    expect(gradient).toHaveAttribute("gradientTransform", "rotate(45)");
  });
});
