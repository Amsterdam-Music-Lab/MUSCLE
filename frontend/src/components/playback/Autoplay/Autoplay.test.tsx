/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import styles from "./Autoplay.module.scss";
import Autoplay from "./Autoplay";

vi.mock("@/components/ui", () => ({
  Countdown: () => <div data-testid="mock-countdown">Mock Countdown</div>,
  Circle: ({ onFinish, children }) => (
    <div data-testid="mock-circle" onClick={onFinish}>
      {children}
    </div>
  ),
}));

vi.mock("../Spectrum", () => ({
  Spectrum: () => <div data-testid="mock-spectrum">Mock Spectrum</div>,
}));

describe("Autoplay Component", () => {
  const mockPlaySection = vi.fn();
  const mockOnFinish = vi.fn();

  const defaultProps = {
    playSection: mockPlaySection,
    onFinish: mockOnFinish,
    duration: 5000,
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders correctly", () => {
    const { container, getByTestId } = render(<Autoplay {...defaultProps} />);
    expect(container.querySelector(`.${styles.autoplay}`)).toBeTruthy();
    expect(getByTestId("mock-circle")).toBeTruthy();
    expect(screen.queryByTestId("mock-countdown")).not.toBeInTheDocument();
    expect(getByTestId("mock-spectrum")).toBeTruthy();
  });

  it("only shows countdown when showSpectrum is false", () => {
    const { queryByTestId } = render(
      <Autoplay {...defaultProps} showSpectrum={false} />
    );
    expect(queryByTestId("mock-spectrum")).not.toBeInTheDocument();
    expect(queryByTestId("mock-countdown")).toBeTruthy();
  });

  it("shows the icon when both showSpectrum and showCountdown are false", () => {
    const { container, queryByTestId } = render(
      <Autoplay {...defaultProps} showSpectrum={false} showCountdown={false} />
    );
    expect(queryByTestId("mock-spectrum")).not.toBeInTheDocument();
    expect(queryByTestId("mock-countdown")).not.toBeInTheDocument();
    expect(container.querySelector(`.${styles.icon}`)).toBeTruthy();
  });

  it("does not show the countdown when duration is not set", () => {
    const { queryByTestId } = render(
      <Autoplay {...defaultProps} showSpectrum={false} duration={undefined} />
    );
    expect(queryByTestId("mock-spectrum")).not.toBeInTheDocument();
    expect(queryByTestId("mock-countdown")).not.toBeInTheDocument();
  });

  it("calls playSection on mount", () => {
    render(<Autoplay {...defaultProps} />);
    expect(mockPlaySection).toHaveBeenCalledWith(0);
  });

  it("calls onFinish when Circle onFinish is triggered", () => {
    render(<Autoplay {...defaultProps} />);
    const mockCircle = screen.getByTestId("mock-circle");
    mockCircle.click();
    expect(mockOnFinish).toHaveBeenCalled();
  });

  it("renders message when provided", () => {
    const message = "Test message";
    render(<Autoplay {...defaultProps} message={message} />);
    expect(screen.getByText(message)).toBeTruthy();
  });

  it("applies custom className", () => {
    const customClass = "custom-class";
    const { container } = render(
      <Autoplay {...defaultProps} className={customClass} />
    );
    const listenDiv = container.querySelector(`.${styles.autoplay}`);
    expect(listenDiv.classList.contains(customClass)).toBe(true);
  });
});
