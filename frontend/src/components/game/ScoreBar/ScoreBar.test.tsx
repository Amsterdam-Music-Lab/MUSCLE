/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { it, describe, expect } from "vitest";
import { screen } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import ScoreBar from "./ScoreBar";
import styles from "./ScoreBar.module.scss";

describe("ScoreBar", () => {
  it("renders correctly with default props", () => {
    render(<ScoreBar value={50} />);
    const bar = screen.getByTestId("scorebar");
    expect(bar).toBeTruthy();
    expect(bar?.textContent).toBe("50%");
    expect(bar).toHaveAttribute("aria-valuenow", "50");
    expect(bar).toHaveStyle({ width: "50%" });
  });

  it("applies custom min/max correctly", () => {
    render(<ScoreBar value={75} min={50} max={100} />);
    const bar = screen.getByTestId("scorebar");
    expect(bar?.textContent).toBe("75%");
    expect(bar).toHaveStyle("width: 50%"); // halfway between 50–100
  });

  it("clamps value below min", () => {
    render(<ScoreBar value={-10} min={0} max={100} />);
    const bar = screen.getByTestId("scorebar");
    expect(bar?.textContent).toBe("0%");
    expect(bar).toHaveStyle("width: 0%");
  });

  it("clamps value above max", () => {
    render(<ScoreBar value={120} max={100} />);
    const bar = screen.getByTestId("scorebar");
    expect(bar?.textContent).toBe("100%");
    expect(bar).toHaveStyle("width: 100%");
  });

  it("renders a custom template", () => {
    const { getByText } = render(
      <ScoreBar value={42} template="Score: {{roundedValue}} / 100" />
    );
    expect(getByText("Score: 42 / 100")).toBeInTheDocument();
  });

  it("uses the correct fill variant", () => {
    render(<ScoreBar value={50} variant="secondary" />);
    const bar = screen.getByTestId("scorebar");
    expect(bar).toHaveClass("fill-secondary");
  });

  it("has animation class when animate is true", () => {
    const { container } = render(<ScoreBar value={30} animate={true} />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.classList).toContain(styles.animate);
  });

  it("omits animation class when animate is false", () => {
    const { container } = render(<ScoreBar value={30} animate={false} />);
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.classList).not.toContain(styles.animate);
  });

  it("sets correct accessibility attributes", () => {
    const { container } = render(<ScoreBar value={42} min={0} max={100} />);
    const bar = container.querySelector('[role="progressbar"]');
    expect(bar).toHaveAttribute("aria-valuenow", "42");
    expect(bar).toHaveAttribute("aria-valuemin", "0");
    expect(bar).toHaveAttribute("aria-valuemax", "100");
  });
});
