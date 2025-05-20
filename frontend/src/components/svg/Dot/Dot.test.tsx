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
import Dot from "./Dot";
import { useVariantFill } from "@/hooks/useVariantFill";

describe("Dot", () => {
  it("renders with default size and black fill", () => {
    const { container } = render(<Dot />);
    const svg = container.querySelector("svg");
    expect(svg).toHaveAttribute("width", "20");
  });

  it("respects size prop", () => {
    const { container } = render(<Dot size={40} />);
    const svg = container.querySelector("svg");
    expect(svg).toHaveAttribute("width", "40");
    expect(svg).toHaveAttribute("height", "40");
  });

  it("adds animation class if animate=true", () => {
    const { container } = render(<Dot animate />);
    const circle = container.querySelector("circle");
    expect(circle?.classList.contains("animate-rotate")).toBe(true);
  });

  it("renders with gradient fill", () => {
    const gradientFill = {
      startColor: "#ff0",
      endColor: "#f00",
      angle: 45,
    };

    const { container } = render(<Dot fill={gradientFill} />);
    const circle = container.querySelector("circle");
    const defs = container.querySelector("defs");

    expect(defs?.querySelector("linearGradient")).toBeTruthy();
    expect(circle?.getAttribute("fill")).toMatch(/^url\(#gradient-/);
  });

  it("uses variant fill if no fill is provided", () => {
    vi.mock("@/hooks/useVariantFill", () => ({
      useVariantFill: vi.fn(() => "#abc"),
    }));
    const { container } = render(<Dot variant="primary" />);
    const circle = container.querySelector("circle");
    expect(useVariantFill).toHaveBeenCalledWith("primary");
    expect(circle?.getAttribute("fill")).toBe("#abc");
  });
});
