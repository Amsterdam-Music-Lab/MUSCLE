/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import ImagePlayer from "./ImagePlayer";
import { MultiPlayerProps } from "../MultiPlayer";

// Mock the MultiPlayer component
function MultiPlayerMock({
  numSections,
  extraContent,
}: Partial<MultiPlayerProps>) {
  return (
    <div data-testid="multiplayer">
      {[...Array(numSections).keys()].map(
        (index) => extraContent && extraContent(index)
      )}
    </div>
  );
}

vi.mock("../MultiPlayer", () => ({
  MultiPlayer: MultiPlayerMock,
}));

describe("ImagePlayer Component", () => {
  const mockPlaySection = vi.fn();
  const mockImages = ["image1.jpg", "image2.jpg"];
  const mockLabels = ["Label 1", "Label 2"];

  const defaultProps = {
    numSections: 2,
    images: mockImages,
    playSection: mockPlaySection,
  };

  it("renders MultiPlayer with correct props", () => {
    const { getByTestId } = render(<ImagePlayer {...defaultProps} />);
    const multiPlayer = getByTestId("multiplayer");
    expect(multiPlayer).toBeTruthy();
  });

  it("renders images correctly", () => {
    render(<ImagePlayer {...defaultProps} />);
    const images = screen.getAllByAltText("PlayerImage");
    expect(images.length).toBe(mockImages.length);
    expect(images[0].getAttribute("src")).toBe(mockImages[0]);
    expect(images[1].getAttribute("src")).toBe(mockImages[1]);
  });

  it("calls playSection when image is clicked", () => {
    render(<ImagePlayer {...defaultProps} />);
    const images = screen.getAllByAltText("PlayerImage");
    fireEvent.click(images[0]);
    expect(mockPlaySection).toHaveBeenCalledWith(0);
  });

  it("renders labels when provided", () => {
    render(<ImagePlayer {...defaultProps} imageLabels={mockLabels} />);
    const labels = screen.getAllByText(/Label \d/);
    expect(labels.length).toBe(mockLabels.length);
    expect(labels[0].textContent).toBe(mockLabels[0]);
    expect(labels[1].textContent).toBe(mockLabels[1]);
  });

  it("displays warning when no images are provided", () => {
    render(<ImagePlayer {...defaultProps} images={[]} />);
    const warning = screen.getAllByText("Warning: No images found");
    expect(warning.length).toBe(2);
  });

  it("displays warning for out-of-range index", () => {
    const props = {
      ...defaultProps,
      images: ["image1.jpg"],
    };

    render(<ImagePlayer {...props} />);
    const warning = screen.getByText(
      "Warning: No spectrograms available for index 1"
    );
    expect(warning).toBeTruthy();
  });
});
