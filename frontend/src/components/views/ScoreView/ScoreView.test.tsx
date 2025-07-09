/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { act } from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import ScoreView from "./ScoreView";
import makeDefaultScoreProps from "@/util/testUtils/makeDefaultScoreProps";
import { vi, describe, expect, it } from "vitest";

vi.useFakeTimers();

describe("ScoreView component", () => {
  it("renders correctly", () => {
    const props = {
      last_song: "Test Song",
      score: 10,
      score_message: "Great job!",
      total_score: 50,
      texts: { score: "Score", next: "Next" },
      icon: null,
      feedback: "Well done!",
      timer: null,
      onNext: vi.fn(),
    };

    render(<ScoreView {...props} />);
    expect(document.body.contains(screen.getByText("Great job!"))).toBe(true);
    expect(document.body.contains(screen.getByText("Test Song"))).toBe(true);
  });

  it("calls onNext after timer duration", () => {
    const onNext = vi.fn();
    render(
      <ScoreView {...{ ...makeDefaultScoreProps({ timer: 5, onNext }) }} />
    );

    act(() => {
      vi.advanceTimersByTime(5000);
    });

    expect(onNext).toHaveBeenCalled();
  });

  it("conditionally renders elements", () => {
    const { rerender } = render(
      <ScoreView {...{ ...makeDefaultScoreProps({ icon: null }) }} />
    );
    expect(
      document.body.contains(screen.queryByTestId("icon-element"))
    ).not.toBeTruthy();

    rerender(
      <ScoreView {...{ ...makeDefaultScoreProps({ last_song: null }) }} />
    );
    expect(
      document.body.contains(screen.queryByText("Test Song"))
    ).not.toBeTruthy();
  });

  it("calls onNext when button is clicked and no timer", () => {
    const onNext = vi.fn();
    render(
      <ScoreView {...{ ...makeDefaultScoreProps({ timer: null, onNext }) }} />
    );

    fireEvent.click(screen.getByText("Next"));
    expect(onNext).toHaveBeenCalled();
  });
});
