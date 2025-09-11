/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { render, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import SmallPlayer from "./SmallPlayer";
import styles from "./SmallPlayer.module.scss";

// Mock the PlayButton component
vi.mock("../PlayButton", () => ({
  PlayButton: ({ ...props }) => (
    <button data-testid="mock-play-button" {...props}>
      Mock Play Button
    </button>
  ),
}));

describe("SmallPlayer Component", () => {
  const mockOnClick = vi.fn();

  const defaultProps = {
    onClick: mockOnClick,
    playing: false,
  };

  it("renders correctly without label", () => {
    const { getByTestId, container } = render(
      <SmallPlayer {...defaultProps} />
    );
    expect(getByTestId("player-small")).toBeTruthy();
    expect(getByTestId("mock-play-button")).toBeTruthy();
    expect(container.querySelector(`.${styles.label}`)).toBeFalsy();
  });

  it("renders correctly with label", () => {
    const label = "Test Label";
    const { getByText } = render(
      <SmallPlayer {...defaultProps} label={label} />
    );
    expect(getByText(label)).toBeTruthy();
  });

  it("applies correct classes", () => {
    const { getByTestId } = render(<SmallPlayer {...defaultProps} />);
    const player = getByTestId("player-small");
    expect(player.classList.contains("transition-appear")).toBe(true);
  });

  it("calls onClick when clicked", () => {
    const { getByTestId } = render(<SmallPlayer {...defaultProps} />);
    const button = getByTestId("mock-play-button");
    fireEvent.click(button);
    expect(mockOnClick).toHaveBeenCalled();
  });

  it("passes correct props to PlayButton", () => {
    const { rerender, getByTestId } = render(<SmallPlayer {...defaultProps} />);
    expect(getByTestId("mock-play-button")).toBeTruthy();
    rerender(<SmallPlayer {...defaultProps} playing={true} disabled={true} />);
    expect(getByTestId("mock-play-button")).toBeTruthy();
  });

  it("renders children", () => {
    const { getByText } = render(
      <SmallPlayer {...defaultProps}>Hello world!</SmallPlayer>
    );
    expect(getByText("Hello world!")).toBeTruthy();
  });
});
