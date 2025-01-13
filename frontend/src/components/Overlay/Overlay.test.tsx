import { vi, describe, it, expect, beforeEach } from "vitest";
import { render, fireEvent, screen, waitFor } from "@testing-library/react";
import Overlay from "./Overlay";

describe("Overlay Component Tests", () => {
  const mockOnClose = vi.fn();
  const defaultProps = {
    isOpen: true,
    onClose: mockOnClose,
    content: <div>Test Content</div>
  };

  beforeEach(() => {
    mockOnClose.mockClear();
  });

  it("should render without crashing", () => {
    render(<Overlay {...defaultProps} />);
    expect(screen.getByText("Test Content")).toBeTruthy();
  });

  it("should render with custom title", () => {
    render(<Overlay {...defaultProps} title="Custom Title" />);
    expect(screen.getByText("Custom Title")).toBeTruthy();
  });

  it("should render with default title when not provided", () => {
    render(<Overlay {...defaultProps} />);
    expect(screen.getByText("Tutorial")).toBeTruthy();
  });

  it("should call onClose when clicking the close button", () => {
    render(<Overlay {...defaultProps} />);
    fireEvent.click(screen.getByLabelText("Close tutorial"));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("should call onClose when clicking the 'Continue' button", () => {
    render(<Overlay {...defaultProps} />);
    waitFor(() => {
      fireEvent.click(screen.getByTitle("Continue"));
      expect(mockOnClose).toHaveBeenCalledTimes(1);
    });
  });

  it("should call onClose when clicking the overlay background", () => {
    render(<Overlay {...defaultProps} />);
    fireEvent.click(screen.getByRole("presentation"));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("should not call onClose when clicking the content area", () => {
    render(<Overlay {...defaultProps} />);
    fireEvent.click(screen.getByText("Test Content"));
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it("should have correct visibility class when isOpen is true", () => {
    render(<Overlay {...defaultProps} />);
    expect(screen.getByRole("presentation").classList.contains("visible")).toBe(true);
  });

  it("should have correct visibility class when isOpen is false", () => {
    render(<Overlay {...defaultProps} isOpen={false} />);
    waitFor(() => {
      expect(screen.getByRole("presentation").classList.contains("visible")).toBe(false);
    });
  });

  it("should have correct aria-hidden attribute based on isOpen", () => {
    const { rerender } = render(<Overlay {...defaultProps} />);
    waitFor(() => {
      expect(screen.getByRole("presentation").getAttribute("aria-hidden")).toBe("false");
    });

    rerender(<Overlay {...defaultProps} isOpen={false} />);
    waitFor(() => {
      expect(screen.getByRole("presentation").getAttribute("aria-hidden")).toBe("true");
    });
  });

  it("should call onClose when pressing Escape key", () => {
    render(<Overlay {...defaultProps} />);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("should not call onClose when pressing other keys", () => {
    render(<Overlay {...defaultProps} />);
    fireEvent.keyDown(document, { key: "Enter" });
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it("should not listen for Escape key when overlay is closed", () => {
    render(<Overlay {...defaultProps} isOpen={false} />);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it("should cleanup event listener on unmount", () => {
    const { unmount } = render(<Overlay {...defaultProps} />);
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
    render(<Overlay {...defaultProps} content={customContent} />);
    expect(screen.getByTestId("custom-content")).toBeTruthy();
    expect(screen.getByText("Custom Title")).toBeTruthy();
    expect(screen.getByText("Custom paragraph")).toBeTruthy();
  });
});
