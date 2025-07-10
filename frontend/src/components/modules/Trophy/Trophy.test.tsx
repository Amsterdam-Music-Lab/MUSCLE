/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import "@testing-library/jest-dom";
import { describe, it, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders.tsx";
import { screen } from "@testing-library/react";
import Trophy from "./Trophy";

describe("Trophy", () => {
  it("renders the provided header and body", () => {
    render(
      <Trophy iconName="star" header="Winner" body="You’ve earned a trophy" />
    );
    expect(screen.getByText("Winner")).toBeInTheDocument();
    expect(screen.getByText("You’ve earned a trophy")).toBeInTheDocument();
  });

  it("shows confetti by default", () => {
    render(<Trophy iconName="star" />);
    expect(
      screen.queryByTestId("confetti-explosion") // you may need to add a `data-testid`
    ).toBeInTheDocument();
  });

  it("does not show confetti if showConfetti is false", () => {
    render(<Trophy iconName="star" showConfetti={false} />);
    expect(
      screen.queryByTestId("confetti-explosion") // you may need to add a `data-testid`
    ).not.toBeInTheDocument();
  });

  it("applies custom class names", () => {
    const { container } = render(
      <Trophy iconName="star" className="custom-class" />
    );
    expect(container.firstChild).toHaveClass("custom-class");
  });

  it("sets CSS vars for wobble angle and duration", () => {
    const { container } = render(
      <Trophy iconName="star" wobbleAngle={10} wobbleDuration={5000} />
    );
    const style = getComputedStyle(container.firstChild as Element);
    expect(style.getPropertyValue("--wobble-angle")).toBe("10deg");
    expect(style.getPropertyValue("--wobble-duration")).toBe("5000ms");
  });
});
