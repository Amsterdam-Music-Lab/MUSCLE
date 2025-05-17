/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import Rank from "./Rank";

describe("Rank Component", () => {
  it("renders the correct components", () => {
    const cup = {
      className: "gold",
      text: "Gold Rank",
    };

    const score = {
      score: 100,
      label: "Points",
    };

    const { getByTestId, getByText } = render(<Rank cup={cup} score={score} />);

    const cupElement = getByTestId("cup");

    // Check if the main div has the correct classes
    expect(cupElement.classList.contains("aha__cup")).toBe(true);
    expect(cupElement.classList.contains("gold")).toBe(true);
    expect(cupElement.classList.contains("offsetCup")).toBe(true);

    // Check if the h4 element contains the correct text
    expect(document.body.contains(getByText("Gold Rank"))).toBe(true);

    // Wait for the score to be rendered
    waitFor(() => {
      expect(document.body.contains(getByText("100 Points"))).toBe(true);
    });
  });
});
