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

// Mock useBoundStore to control backend theme
import useBoundStore from "@/util/stores";
vi.mock("@/util/stores", () => ({
  __esModule: true,
  default: vi.fn(),
}));

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

  it("renders GradientCircles when showGradientCircles is true", () => {
    const { getByTestId } = render(<Page showGradientCircles={true} />);
    expect(getByTestId("gradient-circles")).toBeInTheDocument();
  });

  it("does not render GradientCircles when showGradientCircles is false", () => {
    const { queryByTestId } = render(
      <Page showGradientCircles={false} useBackendTheme={false} />
    );
    expect(queryByTestId("gradient-circles")).toBeNull();
  });

  it("renders background image when showBackgroundImage and backgroundUrl are set", () => {
    const url = "https://example.com/bg.jpg";
    const { getByTestId } = render(
      <Page
        showBackgroundImage={true}
        backgroundUrl={url}
        useBackendTheme={false}
      />
    );
    expect(getByTestId("background-image")).toHaveStyle(
      `background-image: url("${url}")`
    );
  });

  it("does not render background image when showBackgroundImage is false", () => {
    const { queryByTestId } = render(
      <Page showBackgroundImage={false} backgroundUrl="bg.jpg" />
    );
    expect(queryByTestId("background-image")).toBeNull();
  });

  it("applies custom className to the main div", () => {
    const { container } = render(<Page className="custom-class">Content</Page>);
    expect(container.querySelector(".custom-class")).toBeTruthy();
  });

  it("renders background image from backend theme when useBackendTheme is true and backendTheme.backgroundUrl is set", () => {
    useBoundStore.mockImplementation((selector) =>
      selector({ theme: { backgroundUrl: "backend.jpg" } })
    );
    const { getByTestId } = render(
      <Page
        useBackendTheme={true}
        showBackgroundImage={true}
        backgroundUrl="frontend.jpg"
      />
    );
    expect(getByTestId("background-image")).toHaveStyle(
      'background-image: url("backend.jpg")'
    );
  });

  it("does NOT render background image if backendTheme.backgroundUrl is falsy", () => {
    useBoundStore.mockImplementation((selector) =>
      selector({ theme: { backgroundUrl: "" } })
    );
    const { queryByTestId } = render(
      <Page
        showBackgroundImage={true}
        backgroundUrl="https://frontend.com/bg.jpg"
        useBackendTheme={true}
      />
    );
    expect(queryByTestId("background-image")).toBeNull();
  });

  it("renders background image if backendTheme.backgroundUrl is set, even if backgroundUrl prop is falsy", () => {
    useBoundStore.mockImplementation((selector) =>
      selector({ theme: { backgroundUrl: "https://backend.com/bg.jpg" } })
    );
    const { getByTestId } = render(
      <Page showBackgroundImage={true} backgroundUrl="" />
    );
    const bgImg = getByTestId("background-image");
    expect(bgImg).toHaveStyle(
      'background-image: url("https://backend.com/bg.jpg")'
    );
  });

  it("renders background image if useBackendTheme is false, regardless of backendTheme", () => {
    useBoundStore.mockImplementation((selector) =>
      selector({ theme: { backgroundUrl: "https://backend.com/bg.jpg" } })
    );
    const { getByTestId } = render(
      <Page
        showBackgroundImage={true}
        backgroundUrl="https://frontend.com/bg.jpg"
        useBackendTheme={false}
      />
    );
    const bgImg = getByTestId("background-image");
    expect(bgImg).toHaveStyle(
      'background-image: url("https://frontend.com/bg.jpg")'
    );
  });
});
