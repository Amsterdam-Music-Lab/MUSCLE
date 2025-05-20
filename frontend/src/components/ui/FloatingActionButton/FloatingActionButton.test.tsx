/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { vi, it, describe, expect } from "vitest";
import { render } from "@testing-library/react";
import FloatingActionButton from "./FloatingActionButton";
import styles from "./FloatingActionButton.module.scss";

vi.mock("../Overlay", () => ({
  __esModule: true,
  Overlay: ({ Handle, children, ...props }: any) => (
    <div data-testid="overlay" {...props}>
      {Handle ? <Handle {...props} /> : null}
      {children}
    </div>
  ),
}));

describe("FloatingActionButton", () => {
  it("renders with the default icon and position", () => {
    const { getByTestId } = render(
      <FloatingActionButton>Test Content</FloatingActionButton>
    );
    const button = getByTestId("floating-action-button");
    const icon = getByTestId("floating-action-icon");
    expect(button).toBeInTheDocument();
    expect(icon.classList.contains("fa-comment")).toBe(true);
    expect(button.classList.contains(styles.right)).toBe(true);
    expect(button.classList.contains(styles.bottom)).toBe(true);
  });

  it("renders with a custom icon and position", () => {
    const { getByTestId } = render(
      <FloatingActionButton icon="fa-star" position="bottom-left">
        Test Content
      </FloatingActionButton>
    );
    const button = getByTestId("floating-action-button");
    const icon = getByTestId("floating-action-icon");
    expect(icon.classList.contains("fa-star")).toBe(true);
    expect(button.classList.contains(styles.left)).toBe(true);
    expect(button.classList.contains(styles.bottom)).toBe(true);
  });

  it("applies custom className and variant", () => {
    const { getByTestId } = render(
      <FloatingActionButton className="custom-class" variant="secondary">
        Test Content
      </FloatingActionButton>
    );
    const button = getByTestId("floating-action-button");
    expect(button.classList.contains("custom-class")).toBe(true);
    expect(button.classList.contains("fill-secondary")).toBe(true);
  });

  it("renders children inside the overlay", () => {
    const { getByTestId } = render(
      <FloatingActionButton>
        <div data-testid="test-children">Content</div>
      </FloatingActionButton>
    );
    expect(getByTestId("test-children")).toBeInTheDocument();
  });
});
