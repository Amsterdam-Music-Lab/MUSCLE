/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, it, expect, vi, Mock } from "vitest";
import CountDown from "./CountDown";
import Timer from "@/util/timer";

// Mock the Timer utility
vi.mock("@/util/timer", () => ({
  __esModule: true,
  default: vi.fn(),
}));

const MockedTimer = Timer as Mock;

describe("CountDown", () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  it("should display the initial countdown value", () => {
    render(<CountDown duration={10} />);

    const score = screen.getByText("10");
    expect(document.body.contains(score)).toBe(true);
  });

  it("should start the timer when running is true", async () => {
    const mockTimer = vi.fn();
    MockedTimer.mockImplementation(mockTimer);

    render(<CountDown duration={10} running={true} />);

    expect(mockTimer).toHaveBeenCalled();
  });

  it("should not start the timer when running is false", () => {
    const mockTimer = vi.fn();
    MockedTimer.mockImplementation(mockTimer);

    render(<CountDown duration={10} running={false} />);

    expect(mockTimer).not.toHaveBeenCalled();
  });

  it("should update the countdown value as the timer progresses", async () => {
    let onTickCallback: (time: number) => void;
    MockedTimer.mockImplementation(({ onTick }) => {
      onTickCallback = onTick;
      return vi.fn();
    });

    render(<CountDown duration={10} running={true} />);

    await waitFor(() => {
      const score = screen.getByText("10");
      expect(document.body.contains(score)).toBe(true);
    });

    // Simulate timer ticks
    onTickCallback!(5);
    await waitFor(() => {
      const score = screen.getByText("5");
      expect(document.body.contains(score)).toBe(true);
    });

    onTickCallback!(9.5);
    await waitFor(() => {
      const score = screen.getByText("1");
      expect(document.body.contains(score)).toBe(true);
    });
  });

  it("should display 0 when the timer finishes", async () => {
    let onFinishCallback: () => void;
    MockedTimer.mockImplementation(({ onFinish }) => {
      onFinishCallback = onFinish;
      return vi.fn();
    });

    render(<CountDown duration={10} running={true} />);

    await waitFor(() => {
      const score = screen.getByText("10");
      expect(document.body.contains(score)).toBe(true);
    });

    // Simulate timer finish
    onFinishCallback!();
    await waitFor(() => {
      const score = screen.getByText("0");
      expect(document.body.contains(score)).toBe(true);
    });
  });

  it("should apply the correct classes based on the state", async () => {
    const { getByText: getByText1 } = render(
      <CountDown duration={3} running={true} />
    );
    const firstSpan = getByText1("3");
    expect(firstSpan.getAttribute("data-status")).toBe("running");

    // Mock Timer to immediately finish for the second countdown
    MockedTimer.mockImplementation(({ onFinish }) => {
      onFinish();
      return vi.fn();
    });

    // Second countdown: finished
    const { getByText: getByText2 } = render(
      <CountDown duration={5} running={true} />
    );
    const secondSpan = getByText2("0");
    expect(secondSpan.getAttribute("data-status")).toBe("finished");
  });
});
