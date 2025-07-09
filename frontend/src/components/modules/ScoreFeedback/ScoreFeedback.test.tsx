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
import ScoreFeedback from "./ScoreFeedback";

describe("ScoreFeedback", () => {
  it("renders total score and default label", () => {
    render(<ScoreFeedback totalScore={50} />);
    expect(screen.getByText("50")).toBeInTheDocument();
    expect(screen.getByText("Total score")).toBeInTheDocument();
  });

  it("renders custom label", () => {
    render(<ScoreFeedback totalScore={50} totalScoreLabel="Current score" />);
    expect(screen.getByText("Current score")).toBeInTheDocument();
  });

  it("renders feedback message from children", () => {
    render(<ScoreFeedback>Total score so far!</ScoreFeedback>);
    expect(screen.getByText("Total score so far!")).toBeInTheDocument();
  });

  it("renders positive turn score with + prefix", () => {
    render(<ScoreFeedback turnScore={10} />);
    expect(screen.getByText("+10 points")).toBeInTheDocument();
  });

  it("renders zero turn score message", () => {
    render(<ScoreFeedback turnScore={0} />);
    expect(screen.getByText("You got 0 points.")).toBeInTheDocument();
  });

  it("renders negative turn score", () => {
    render(<ScoreFeedback turnScore={-5} />);
    expect(screen.getByText("-5 points")).toBeInTheDocument();
  });

  it("does not render turn score message if undefined", () => {
    render(<ScoreFeedback />);
    expect(screen.queryByText(/points/)).not.toBeInTheDocument();
  });
});
