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
import ScoreDisplay from "./ScoreDisplay";
import styles from "./ScoreDisplay.module.scss";

describe("ScoreDisplay", () => {
  it("renders score with units and label", () => {
    render(<ScoreDisplay score={42} label="Total Score" units="pts" />);
    expect(screen.getByText("42")).toBeInTheDocument();
    expect(screen.getByText("pts")).toBeInTheDocument();
    expect(screen.getByText("Total Score")).toBeInTheDocument();
  });

  it("shows placeholder when score is undefined", () => {
    render(<ScoreDisplay />);
    expect(screen.getByText("??")).toBeInTheDocument();
  });

  it("does not render units when score is undefined", () => {
    render(<ScoreDisplay units="xp" />);
    expect(screen.queryByText("xp")).not.toBeInTheDocument();
  });

  it("renders custom placeholder", () => {
    render(<ScoreDisplay placeholder="n/a" />);
    expect(screen.getByText("n/a")).toBeInTheDocument();
  });

  it("applies text-fill variant class when score is defined", () => {
    render(<ScoreDisplay score={5} variant="secondary" />);
    expect(screen.getByText("5")).toHaveClass("text-fill-secondary");
  });

  it("applies text-light-gray class when score is undefined", () => {
    render(<ScoreDisplay />);
    expect(screen.getByText("??")).toHaveClass("text-light-gray");
  });

  it("applies font size using CSS variable", () => {
    const { container } = render(<ScoreDisplay score={10} size={5} />);
    const root = container.querySelector(`.${styles.scoreDisplay}`)!;
    expect(root.style.getPropertyValue("--score-display-font-size")).toBe("5");
  });
});
