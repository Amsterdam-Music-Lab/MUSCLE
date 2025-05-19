/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { it, describe, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import SquareLayout from "./SquareLayout";

describe("SquareLayout", () => {
  it("renders header, square, footer, and aside sections", () => {
    const { getByText } = render(
      <SquareLayout portraitHeaderHeight={0.5} fullscreen={false}>
        <SquareLayout.Header>Header Content</SquareLayout.Header>
        <SquareLayout.Square>Square Content</SquareLayout.Square>
        <SquareLayout.Footer>Footer Content</SquareLayout.Footer>
        <SquareLayout.Aside>Aside Content</SquareLayout.Aside>
      </SquareLayout>
    );
    expect(getByText("Header Content")).toBeInTheDocument();
    expect(getByText("Square Content")).toBeInTheDocument();
    expect(getByText("Footer Content")).toBeInTheDocument();
    expect(getByText("Aside Content")).toBeInTheDocument();
  });
});
