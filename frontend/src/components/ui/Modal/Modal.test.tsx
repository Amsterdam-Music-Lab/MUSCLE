/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { vi, describe, it, expect, beforeEach } from "vitest";
import { render, fireEvent, screen, waitFor } from "@testing-library/react";
import Modal from "./Modal";
import styles from "./Modal.module.scss";

describe("Modal Component Tests", () => {
  const mockOnClose = vi.fn();
  const defaultProps = {
    open: true,
    onClose: mockOnClose,
    closeButtonText: "Close",
    children: <div>Test Content</div>,
  };

  beforeEach(() => {
    mockOnClose.mockClear();
  });

  it("should render without crashing", () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByText("Test Content")).toBeTruthy();
  });

  it("should render with custom title", () => {
    render(<Modal {...defaultProps} title="Custom Title" />);
    expect(screen.getByText("Custom Title")).toBeTruthy();
  });

  it("should call onClose when clicking the close button", () => {
    render(<Modal {...defaultProps} />);
    fireEvent.click(screen.getByLabelText("Close"));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("should call onClose when clicking the 'Continue' button", () => {
    render(<Modal {...defaultProps} />);
    waitFor(() => {
      fireEvent.click(screen.getByTitle("Continue"));
      expect(mockOnClose).toHaveBeenCalledTimes(1);
    });
  });

  it("should call onClose when clicking the overlay background", () => {
    render(<Modal {...defaultProps} />);
    fireEvent.click(screen.getByRole("presentation"));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("should not call onClose when clicking the content area", () => {
    render(<Modal {...defaultProps} />);
    fireEvent.click(screen.getByText("Test Content"));
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it("should have correct visibility class when isOpen is true", () => {
    render(<Modal {...defaultProps} />);
    expect(
      screen.getByRole("presentation").classList.contains(styles.active)
    ).toBe(true);
  });

  it("should have correct visibility class when open is false", () => {
    render(<Modal {...defaultProps} open={false} />);
    waitFor(() => {
      expect(
        screen.getByRole("presentation").classList.contains(styles.active)
      ).toBe(false);
    });
  });

  it("should have correct aria-hidden attribute based on isOpen", () => {
    const { rerender } = render(<Modal {...defaultProps} />);
    waitFor(() => {
      expect(screen.getByRole("presentation").getAttribute("aria-hidden")).toBe(
        "false"
      );
    });

    rerender(<Modal {...defaultProps} isOpen={false} />);
    waitFor(() => {
      expect(screen.getByRole("presentation").getAttribute("aria-hidden")).toBe(
        "true"
      );
    });
  });

  it("should call onClose when pressing Escape key", () => {
    render(<Modal {...defaultProps} />);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("should not call onClose when pressing other keys", () => {
    render(<Modal {...defaultProps} />);
    fireEvent.keyDown(document, { key: "Enter" });
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it("should not listen for Escape key when overlay is closed", () => {
    render(<Modal {...defaultProps} open={false} />);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it("should cleanup event listener on unmount", () => {
    const { unmount } = render(<Modal {...defaultProps} />);
    unmount();
    fireEvent.keyDown(document, { key: "Escape" });
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it("should render custom content correctly", () => {
    const customContent = (
      <div data-testid="custom-content">
        <h3>Custom Title</h3>
        <p>Custom paragraph</p>
      </div>
    );
    render(<Modal {...defaultProps}>{customContent}</Modal>);
    expect(screen.getByTestId("custom-content")).toBeTruthy();
    expect(screen.getByText("Custom Title")).toBeTruthy();
    expect(screen.getByText("Custom paragraph")).toBeTruthy();
  });

  it("renders and uses a custom Handle component", () => {
    const mockHandle = vi.fn();

    const CustomHandle = ({ onClick }: { onClick: () => void }) => (
      <button
        data-testid="custom-handle"
        onClick={() => {
          mockHandle();
          onClick();
        }}
      >
        Open Modal
      </button>
    );

    render(
      <Modal open={false} Handle={CustomHandle} closeButtonText="Close" />
    );

    // The custom handle should be rendered
    const handleButton = screen.getByTestId("custom-handle");
    expect(handleButton).toBeInTheDocument();
    handleButton.click();
    expect(mockHandle).toHaveBeenCalled();
  });
});
