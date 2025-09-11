/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { act } from "react";
import { screen } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import { vi, describe, it, expect } from "vitest";
import ExplainerView from "./ExplainerView";

describe("ExplainerView Component", () => {
  const props = {
    instruction: "Some instruction",
    button_label: "Next",
    steps: [],
    onNext: vi.fn(),
    timer: 1,
  };

  it("renders with given props", () => {
    render(<ExplainerView {...props} />);
    expect(screen.getByTestId("explainer")).toBeTruthy();
  });

  it("renders the instruction message", async () => {
    render(<ExplainerView {...props} />);
    await screen.findByText("Some instruction");
  });

  it("renders the button with correct label and triggers onNext on click", async () => {
    const onNext = vi.fn();
    render(<ExplainerView {...props} onNext={onNext} />);
    const button = screen.getByRole("button", { name: "Next" });
    expect(button).toBeInTheDocument();
    await act(() => button.click());
    expect(onNext).toHaveBeenCalled();
  });

  it("renders all steps when steps are provided", () => {
    const steps = [
      { number: 1, description: "Step one" },
      { number: 2, description: "Step two" },
    ];
    render(<ExplainerView {...props} steps={steps} />);
    expect(screen.getByText("Step one")).toBeInTheDocument();
    expect(screen.getByText("Step two")).toBeInTheDocument();
  });

  it("calls onNext automatically after timer expires", async () => {
    vi.useFakeTimers();
    const onNext = vi.fn();
    render(<ExplainerView {...props} timer={500} onNext={onNext} />);
    vi.advanceTimersByTime(500);
    expect(onNext).toHaveBeenCalled();
    vi.useRealTimers();
  });

  it("does not render steps list when steps is empty", () => {
    render(<ExplainerView {...props} steps={[]} />);
    expect(screen.queryByRole("list")).toBeNull();
  });
});
