/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { BrowserRouter as Router } from "react-router-dom";
import { vi, describe, beforeEach, it, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import AppBar from "./AppBar";

import useBoundStore from "@/util/stores";
vi.mock("@/util/stores", () => ({
  __esModule: true,
  default: vi.fn(),
}));

// Mock Logo to a test div
vi.mock("@/components/svg", () => ({
  Logo: (props: any) => <div data-testid="logo-mock" {...props} />,
}));

describe("AppBar", () => {
  const BASE_URL = "https://www.amsterdammusiclab.nl";

  beforeEach(() => {
    vi.resetModules();
    import.meta.env.VITE_AML_HOME = BASE_URL;
  });

  it("renders correctly", () => {
    const { getByText } = render(<AppBar title="Test Title" />, {
      wrapper: Router,
    });

    const titleElement = getByText("Test Title");
    expect(document.body.contains(titleElement)).toBe(true);
  });

  it("renders logo as Link for relative URL", () => {
    vi.mocked(useBoundStore).mockImplementation((selector) =>
      selector({ theme: { logo: { href: "/relative-path" } } })
    );
    const { getByTestId } = render(<AppBar title="Test Title" />, {
      wrapper: Router,
    });
    const logo = getByTestId("logo-mock");
    expect(logo.closest("a")).toHaveAttribute("href", "/relative-path");
  });

  it("renders logo as an a-element for absolute URL", () => {
    vi.mocked(useBoundStore).mockImplementation((selector) =>
      selector({ theme: { logo: { href: BASE_URL } } })
    );
    const { getByTestId } = render(<AppBar title="Test Title" />, {
      wrapper: Router,
    });
    const logo = getByTestId("logo-mock");
    // The parent <a> should have the correct href
    expect(logo.closest("a")).toHaveAttribute("href", BASE_URL);
  });
});
