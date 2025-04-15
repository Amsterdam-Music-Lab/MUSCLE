/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { it, describe, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import BarPlot from "./BarPlot";

describe("BarPlot", () => {
  it("renders the correct number of bars", () => {
    const data = [1, 2, 3, 4, 5];
    const { container } = render(<BarPlot data={data} />);
    const bars = container.querySelectorAll('[class*="bar"]');
    expect(bars.length).toBe(data.length);
  });

  it("calculates bar height based on data", () => {
    const data = [0, 25, 50, 75, 100];
    const { container } = render(<BarPlot data={data} min={0} max={100} />);
    const bars = container.querySelectorAll('[class*="bar"]');
    const heights = Array.from(bars).map(
      (bar) => (bar as HTMLElement).style.height
    );
    expect(heights).toEqual(["0%", "25%", "50%", "75%", "100%"]);
  });

  it("defaults to min/max from data if not specified", () => {
    const data = [10, 20, 30];
    const { container } = render(<BarPlot data={data} />);
    const bars = container.querySelectorAll('[class*="bar"]');
    const heights = Array.from(bars).map(
      (bar) => (bar as HTMLElement).style.height
    );
    expect(heights).toEqual(["0%", "50%", "100%"]);
  });

  it("applies custom color style when color is given", () => {
    const data = [10, 20];
    const { container } = render(<BarPlot data={data} color="red" />);
    const plot = container.firstChild as HTMLElement;
    expect(plot.style.getPropertyValue("--bar-color")).toBe("red");
  });

  it("uses variant class when no color is specified", () => {
    const data = [10, 20];
    const { container } = render(<BarPlot data={data} variant="secondary" />);
    const bar = container.querySelector('[class*="bar"]');
    expect(bar?.className).toContain("fill-secondary");
  });

  it("applies the correct --num-bars style", () => {
    const data = [1, 2, 3];
    const { container } = render(<BarPlot data={data} />);
    const plot = container.firstChild as HTMLElement;
    expect(plot.style.getPropertyValue("--num-bars")).toBe(
      data.length.toString()
    );
  });
});
