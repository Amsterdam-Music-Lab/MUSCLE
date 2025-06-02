/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { render, screen, fireEvent } from "@testing-library/react";
import { describe, test, expect, beforeEach, vi } from "vitest";
import MultiPlayer from "./MultiPlayer";
import styles from "./MultiPlayer.module.scss";

// Mock the SmallPlayer component
vi.mock("../SmallPlayer", () => ({
  SmallPlayer: ({ label, children, ...props }) => (
    <button data-testid="mock-small-player" {...props}>
      Mock Small Player
      {label && <span>{label}</span>}
      {children}
    </button>
  ),
}));

describe("MultiPlayer Component", () => {
  const mockPlaySection = vi.fn();
  const mockSections = [
    { id: "1", url: "123451" },
    { id: "2", url: "123452" },
    { id: "3", url: "123453" },
  ];

  const defaultProps = {
    playSection: mockPlaySection,
    numSections: 3,
    playerIndex: 0,
    labels: { "0": "Label 1", "1": "Label 2", "2": "Label 3" },
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("renders correct number of PlayerSmall components", () => {
    render(<MultiPlayer {...defaultProps} />);
    const players = screen.getAllByTestId("mock-small-player");
    expect(players.length).toBe(mockSections.length);
  });

  test("applies correct class names", () => {
    const { container } = render(<MultiPlayer {...defaultProps} />);
    expect(container.firstChild).toBeTruthy();
    const classList = container.firstChild.classList;
    expect(classList.contains(styles.multiplayer)).toBe(true);
  });

  test("calls playSection with correct index when PlayerSmall is clicked", () => {
    render(<MultiPlayer {...defaultProps} />);
    const players = screen.getAllByTestId("mock-small-player");
    console.log(players[1]);
    fireEvent.click(players[1]);
    expect(mockPlaySection).toHaveBeenCalledWith(1);
  });

  test("applies correct label to PlayerSmall components", () => {
    const { container } = render(<MultiPlayer {...defaultProps} />);
    console.log(container.innerHTML);
    expect(screen.getByText("Label 1")).toBeTruthy();
    expect(screen.getByText("Label 2")).toBeTruthy();
    expect(screen.getByText("Label 3")).toBeTruthy();
  });

  test("renders extraContent when provided", () => {
    const extraContent = vi.fn((index: string) => {
      console.log(index);
      return <span data-testid={`extra-${index}`}>Extra {index}</span>;
    });
    const { container, getByTestId } = render(
      <MultiPlayer {...defaultProps} extraContent={extraContent} />
    );
    expect(extraContent).toHaveBeenCalled();
    console.log(container.innerHTML);
    expect(getByTestId("extra-0")).toBeTruthy();
    expect(getByTestId("extra-1")).toBeTruthy();
    expect(getByTestId("extra-2")).toBeTruthy();
  });

  test("applies custom styles when provided", () => {
    const customStyle = { "custom-root-class": true };
    const { container } = render(
      <MultiPlayer {...defaultProps} className={customStyle} />
    );
    expect(container.firstChild.classList.contains("custom-root-class")).toBe(
      true
    );
  });
});
