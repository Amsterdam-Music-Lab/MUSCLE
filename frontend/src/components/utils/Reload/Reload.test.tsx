/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { API_BASE_URL } from "@/config";
import Reload from "./Reload";

let mockUseLocation = vi.fn();

// Mock the useLocation hook
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useLocation: () => mockUseLocation(),
  };
});

describe("Reload", () => {
  // Mock window.location
  const originalLocation = window.location;

  beforeEach(() => {
    vi.resetAllMocks();

    mockUseLocation.mockReturnValue({ pathname: "/" });

    // Mock window.location
    delete window.location;
    window.location = { ...originalLocation, href: "" };
  });

  afterEach(() => {
    window.location = originalLocation;
  });

  it("renders without crashing", () => {
    mockUseLocation.mockReturnValue({ pathname: "/" });
    const { getByTestId } = render(
      <MemoryRouter>
        <Reload />
      </MemoryRouter>
    );
    expect(getByTestId("reload")).toBeTruthy();
  });

  it("redirects to the correct URL", () => {
    const testPath = "/test-path";
    mockUseLocation.mockReturnValue({ pathname: testPath });

    render(
      <MemoryRouter initialEntries={[testPath]}>
        <Reload />
      </MemoryRouter>
    );

    expect(window.location.href).toBe(API_BASE_URL + testPath);
  });

  it("uses the current location for redirection", () => {
    const testPath = "/another-path";
    mockUseLocation.mockReturnValue({ pathname: testPath });

    render(
      <MemoryRouter initialEntries={[testPath]}>
        <Reload />
      </MemoryRouter>
    );

    expect(window.location.href).toBe(API_BASE_URL + testPath);
  });
});
