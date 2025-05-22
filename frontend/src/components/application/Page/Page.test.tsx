/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { it, describe, vi, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import Page from "./Page";

// Mock AppBar to inspect props
vi.mock("../AppBar", () => ({
  AppBar: vi.fn(({ title }: { title: string }) => (
    <div data-testid="appbar">{title}</div>
  )),
}));

// Mock GradientCircles to a test div
vi.mock("@/components/svg", () => ({
  GradientCircles: () => <div data-testid="gradient-circles" />,
}));

describe("Page Component Tests", () => {
  it("renders itself with children", async () => {
    const { findByText } = render(<Page>This is a test</Page>);
    await findByText("This is a test");
  });

  it("renders AppBar with the provided title", () => {
    const { getByTestId } = render(
      <Page title="Test Title" showAppBar={true} />
    );
    expect(getByTestId("appbar")).toHaveTextContent("Test Title");
  });

  it("does not render AppBar when showAppBar is false", () => {
    const { queryByText } = render(<Page title="Hidden" showAppBar={false} />);
    expect(queryByText("Hidden")).toBeNull();
  });

  it("applies custom className to the main div", () => {
    const { container } = render(<Page className="custom-class">Content</Page>);
    expect(container.querySelector(".custom-class")).toBeTruthy();
  });
});
