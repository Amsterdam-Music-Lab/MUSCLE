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
import GradientCircles from "./GradientCircles";

describe("GradientCircles", () => {
  it("renders the SVG wrapper component", () => {
    const { container } = render(<GradientCircles />);
    const svg = container.querySelector("svg");
    expect(svg).toBeTruthy();
  });

  it("renders the blur overlay when blur is non-zero", () => {
    const { container } = render(<GradientCircles blur={20} />);
    const blurDiv = container.querySelector('[class*="blur"]');
    expect(blurDiv).toBeTruthy();
  });

  it("does not render the blur overlay when blur is 0", () => {
    const { container } = render(<GradientCircles blur={0} />);
    const blurDiv = container.querySelector('[class*="blur"]');
    expect(blurDiv).toBeFalsy();
  });

  it("applies custom className and inline style", () => {
    const { container } = render(
      <GradientCircles
        className="my-custom-class"
        style={{ zIndex: 99 }}
        blur={10}
      />
    );

    const outerDiv = container.querySelector("div.my-custom-class");
    expect(outerDiv).toBeTruthy();
    expect(outerDiv?.getAttribute("style")).toContain("--blur: 10px");
    expect(outerDiv?.getAttribute("style")).toContain("z-index: 99");
  });

  it("passes props to SVG component", () => {
    const { container } = render(
      <GradientCircles
        animate={true}
        numCircles={5}
        height={300}
        aspect={1.5}
      />
    );

    const svg = container.querySelector("svg");
    expect(svg?.getAttribute("viewBox")).toBe(`0 0 450 300`);
  });
});
