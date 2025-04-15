/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, it, expect, vi, beforeEach, afterEach, Mock } from "vitest";
import { render, act, screen } from "@testing-library/react";
import Histogram from "./Histogram";

// Mock requestAnimationFrame and cancelAnimationFrame
vi.stubGlobal(
  "requestAnimationFrame",
  (callback: FrameRequestCallback): number => {
    return setTimeout(callback, 16); // Approximate 60 FPS
  }
);

vi.stubGlobal("cancelAnimationFrame", (handle: number): void => {
  clearTimeout(handle);
});

// Mock BarPlot to inspect props
vi.mock("@/components/game", () => ({
  BarPlot: (props: any) => (
    <div
      data-testid="barplot"
      data-bars={props.data?.length}
      data-data={JSON.stringify(props.data)}
    >
      Mock BarPlot
    </div>
  ),
}));

// Stub store
vi.mock("@/util/stores", () => ({
  __esModule: true,
  default: (fn: any) =>
    fn({ currentAction: { playback: { play_method: "BUFFER" } } }),
  useBoundStore: vi.fn(),
}));

describe("Histogram", () => {
  let mockAnalyser: {
    getByteFrequencyData: Mock;
  };

  beforeEach(() => {
    // Mock setInterval and clearInterval
    vi.useFakeTimers();

    // Mock the Web Audio API
    mockAnalyser = {
      getByteFrequencyData: vi.fn(),
    };

    (global as any).window.audioContext = {};
    (global as any).window.analyzer = mockAnalyser;
  });

  afterEach(() => {
    vi.clearAllTimers();
    vi.restoreAllMocks();
  });

  it("renders the correct number of bars", () => {
    render(<Histogram bars={5} />);
    const plot = screen.getByTestId("barplot");
    expect(plot).toHaveAttribute("data-bars", "5");
  });

  it("generates random data when random=true", async () => {
    render(<Histogram bars={5} random={true} interval={100} />);
    const plot = screen.getByTestId("barplot");
    const initial = JSON.parse(plot.getAttribute("data-data")!);

    await act(() => {
      vi.advanceTimersByTime(100);
    });

    const updated = JSON.parse(plot.getAttribute("data-data")!);
    expect(updated).not.toEqual(initial); // Data should change
  });

  it("resets data when running=false", () => {
    render(<Histogram bars={4} running={false} />);
    const plot = screen.getByTestId("barplot");
    const data = JSON.parse(plot.getAttribute("data-data")!);
    expect(data).toEqual([0, 0, 0, 0]);
  });

  it("uses analyzer when available and random=false", async () => {
    const fakeData = new Uint8Array([11, 22, 33, 44, 55, 66, 77, 88]);
    const mockGetData = vi.fn((arr: Uint8Array) => arr.set(fakeData));
    (window as any).analyzer = { getByteFrequencyData: mockGetData };
    (window as any).audioContext = {}; // just to satisfy the check

    render(<Histogram bars={5} random={false} />);
    await act(() => {
      vi.advanceTimersByTime(16);
    });

    const plot = screen.getByTestId("barplot");
    const data = JSON.parse(plot.getAttribute("data-data")!);
    expect(data.length).toBe(5);
    expect(mockGetData).toHaveBeenCalled();
  });

  it("falls back to zero data if no analyzer is available", () => {
    delete (window as any).analyzer;
    render(<Histogram bars={3} random={false} />);
    const plot = screen.getByTestId("barplot");
    const data = JSON.parse(plot.getAttribute("data-data")!);
    expect(data).toEqual([0, 0, 0]);
  });

  it.skip("has active class when running", () => {
    const { container } = render(<Histogram running={true} />);
    const histogram = container.querySelector(".aha__histogram");

    if (!histogram) {
      throw new Error("Histogram not found");
    }

    expect(histogram.classList.contains("active")).toBe(true);
  });

  it.skip("does not have active class when not running", () => {
    const { container } = render(<Histogram running={false} />);
    const histogram = container.querySelector(".aha__histogram");

    if (!histogram) {
      throw new Error("Histogram not found");
    }

    expect(histogram.classList.contains("active")).toBe(false);
  });

  it.skip("updates bar heights based on frequency data when running", async () => {
    const bars = 5;
    mockAnalyser.getByteFrequencyData.mockImplementation((array) => {
      for (let i = 0; i < array.length; i++) {
        array[i] = Math.floor(Math.random() * 256);
      }
    });

    const { container, rerender } = render(
      <Histogram running={true} bars={bars} />
    );

    const getHeights = () =>
      Array.from(container.querySelectorAll(".aha__histogram > div")).map(
        (bar) => bar.style.height
      );

    const initialHeights = getHeights();

    // Advance timers and trigger animation frame
    await act(async () => {
      vi.advanceTimersByTime(100);
    });

    rerender(<Histogram running={true} bars={bars} />);

    const updatedHeights = getHeights();

    expect(initialHeights).not.to.deep.equal(updatedHeights);
    expect(mockAnalyser.getByteFrequencyData).toHaveBeenCalled();
  });

  it.skip("does not update bar heights when not running", () => {
    const bars = 5;
    mockAnalyser.getByteFrequencyData.mockImplementation(() => {
      // This should not be called when running is false
    });

    const { container } = render(<Histogram running={false} bars={bars} />);

    const getHeights = () =>
      Array.from(container.querySelectorAll(".aha__histogram > div")).map(
        (bar) => bar.style.height
      );

    const initialHeights = getHeights();

    // Advance timers to simulate time passing
    act(() => {
      vi.advanceTimersByTime(1000); // Advance time by 1 second
    });

    const updatedHeights = getHeights();

    expect(initialHeights).to.deep.equal(updatedHeights);
    expect(mockAnalyser.getByteFrequencyData).not.toHaveBeenCalled();
  });

  it.skip("updates bar heights based on random data when random is true and running is true", async () => {
    const bars = 5;

    const { container, rerender } = render(
      <Histogram running={true} bars={bars} random={true} interval={200} />
    );

    const getHeights = () =>
      Array.from(container.querySelectorAll(".aha__histogram > div")).map(
        (bar) => bar.style.height
      );

    const initialHeights = getHeights();

    // Advance timers by at least one interval
    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    rerender(<Histogram running={true} bars={bars} random={true} />);

    const updatedHeights = getHeights();

    expect(initialHeights).not.to.deep.equal(updatedHeights);
  });

  it.skip("does not call getByteFrequencyData when random is true", async () => {
    const bars = 5;

    const { rerender } = render(
      <Histogram running={true} bars={bars} random={true} />
    );

    // Advance timers and trigger animation frame
    await act(async () => {
      vi.advanceTimersByTime(100);
    });

    rerender(<Histogram running={true} bars={bars} random={true} />);

    expect(mockAnalyser.getByteFrequencyData).not.toHaveBeenCalled();
  });

  it.skip("updates bar heights based on random data at the specified interval", async () => {
    const bars = 5;
    const interval = 200;

    const { container } = render(
      <Histogram running={true} bars={bars} random={true} interval={interval} />
    );

    const getHeights = () =>
      Array.from(container.querySelectorAll(".aha__histogram > div")).map(
        (bar) => bar.style.height
      );

    const initialHeights = getHeights();

    // Advance timers by the interval to trigger the update
    await act(async () => {
      vi.advanceTimersByTime(interval);
    });

    const updatedHeights = getHeights();

    expect(initialHeights).not.to.deep.equal(updatedHeights);
  });

  it.skip("updates bar heights based on frequency data using requestAnimationFrame", async () => {
    const bars = 5;

    mockAnalyser.getByteFrequencyData.mockImplementation((array) => {
      for (let i = 0; i < array.length; i++) {
        array[i] = Math.floor(Math.random() * 256);
      }
    });

    const { container } = render(<Histogram running={true} bars={bars} />);

    const getHeights = () =>
      Array.from(container.querySelectorAll(".aha__histogram > div")).map(
        (bar) => bar.style.height
      );

    const initialHeights = getHeights();

    // Advance timers to simulate requestAnimationFrame calls
    await act(async () => {
      vi.advanceTimersByTime(16); // Approximate time for one frame at 60 FPS
    });

    const updatedHeights = getHeights();

    expect(initialHeights).not.to.deep.equal(updatedHeights);
    expect(mockAnalyser.getByteFrequencyData).toHaveBeenCalled();
  });
});
