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

vi.mock("@/components/ui", () => ({
  __esModule: true,
  Modal: ({ Handle, children, ...props }: any) => (
    <div data-testid="modal" {...props}>
      {Handle ? <Handle {...props} /> : null}
      {children}
    </div>
  ),
}));

vi.mock("@/components/icons", () => ({
  Icon: (props) => (
    <i data-testid="mock-icon" data-props={JSON.stringify(props)} />
  ),
}));

describe("FloatingActionButton", () => {
  it("renders with the default icon and position", () => {
    const { getByTestId } = render(
      <FloatingActionButton>Test Content</FloatingActionButton>
    );
    const button = getByTestId("floating-action-button");
    const icon = getByTestId("mock-icon");
    const props = JSON.parse(icon.getAttribute("data-props")!);
    expect(props.name).toBe("comment");
    expect(button.classList.contains(styles.right)).toBe(true);
    expect(button.classList.contains(styles.bottom)).toBe(true);
  });

  it("renders with a custom icon and position", () => {
    const { getByTestId } = render(
      <FloatingActionButton iconName="facebook" position="bottom-left">
        Test Content
      </FloatingActionButton>
    );
    const button = getByTestId("floating-action-button");
    const icon = getByTestId("mock-icon");
    const props = JSON.parse(icon.getAttribute("data-props")!);
    expect(props.name).toBe("facebook");
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

  it("renders children inside the modal", () => {
    const { getByTestId } = render(
      <FloatingActionButton>
        <div data-testid="test-children">Content</div>
      </FloatingActionButton>
    );
    expect(getByTestId("test-children")).toBeInTheDocument();
  });
});
