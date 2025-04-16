/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { vi, describe, expect, it } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import Star from "./Star";

describe("Star", () => {
  beforeEach(() => {
    vi.mock("@/hooks/useVariantFill", () => ({
      useVariantFill: vi.fn(() => "#123456"),
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders SVG with default props", () => {
    const { container } = render(<Star />);
    const svg = container.querySelector("svg");
    const path = container.querySelector("path");
    expect(svg).toBeTruthy();
    expect(path).toBeTruthy();
    expect(svg?.getAttribute("viewBox")).toBe("0 0 20 20");
  });

  test("applies animate-rotate class when animate=true", () => {
    const { container } = render(<Star animate />);
    const group = container.querySelector("g");
    expect(group?.classList.contains("animate-rotate")).toBe(true);
  });

  test("renders a circle and mask when showCircle is true", () => {
    const { container } = render(<Star showCircle />);
    const defs = container.querySelector("defs");
    const circle = defs?.querySelector("circle");
    const mask = defs?.querySelector("mask");
    expect(circle).toBeTruthy();
    expect(mask).toBeTruthy();

    const use = container.querySelector("g use");
    expect(use?.getAttribute("mask")).toMatch(/^url\(#mask-/);
  });

  test("does not render mask or circle if showCircle is false", () => {
    const { container } = render(<Star showCircle={false} />);
    const defs = container.querySelector("defs");
    const mask = defs?.querySelector("mask");
    const circle = defs?.querySelector("circle");
    expect(mask).toBeFalsy();
    expect(circle).toBeFalsy();
  });

  test("uses gradient if fill is an object", () => {
    const gradientFill = {
      startColor: "#f00",
      endColor: "#0f0",
      angle: 45,
    };
    const { container } = render(<Star fill={gradientFill} />);
    const gradient = container.querySelector("linearGradient");
    expect(gradient).toBeTruthy();
    const use = container.querySelector("g use");
    expect(use?.getAttribute("fill")).toMatch(/^url\(#circle-gradient-/);
  });

  test("uses gradient for starFill if it is an object", () => {
    const gradientFill = {
      startColor: "#f00",
      endColor: "#00f",
      angle: 90,
    };
    const { container } = render(<Star starFill={gradientFill} />);
    const path = container.querySelector("path");
    expect(path?.getAttribute("fill")).toMatch(/^url\(#star-gradient-/);
  });

  test("uses variant color if no fill is passed", () => {
    const { container } = render(<Star />);
    const use = container.querySelector("g use");
    expect(use?.getAttribute("fill")).toBe("#123456");
  });
});
