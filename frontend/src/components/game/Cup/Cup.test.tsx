/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { render } from "@testing-library/react";
import Cup from "./Cup";
import { describe, expect, it } from "vitest";

describe("Cup Component", () => {
  it("renders with the correct class and text", () => {
    const rank = {
      className: "gold",
      text: "Gold Cup",
    };

    const { getByTestId, getByText } = render(<Cup {...rank} />);

    const cupElement = getByTestId("cup");

    // Check if the main div has the correct classes
    expect(cupElement.classList.contains("aha__cup")).toBe(true);
    expect(cupElement.classList.contains("gold")).toBe(true);
    expect(cupElement.classList.contains("offsetCup")).toBe(true);

    // Check if the h4 element contains the correct text
    expect(document.body.contains(getByText("Gold Cup"))).toBe(true);
  });

  it("does not have offsetCup class when text is empty", () => {
    const rank = {
      className: "silver",
      text: "",
    };

    const { getByTestId } = render(<Cup {...rank} />);

    const cupElement = getByTestId("cup");

    // Check if the main div has the correct classes
    expect(cupElement.classList.contains("aha__cup")).toBe(true);
    expect(cupElement.classList.contains("silver")).toBe(true);
    expect(cupElement.classList.contains("offsetCup")).toBe(false);

    // Check if the h4 element contains the correct text
    const cupText = getByTestId("cup-text");
    expect(document.body.contains(cupText)).toBe(true);
    expect(cupText.textContent).toBe("");
  });

  it("renders the cup div", () => {
    const rank = {
      className: "bronze",
      text: "Bronze Cup",
    };

    const { getByTestId } = render(<Cup {...rank} />);

    const cupElement = getByTestId("cup-animation");

    // Check if the cup div is present
    expect(document.body.contains(cupElement)).toBe(true);
  });
});
