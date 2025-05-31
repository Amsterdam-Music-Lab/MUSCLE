/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, it, expect, vi } from "vitest";
import InternalRedirect from "./InternalRedirect";
import { routes } from "@/config";

// Mock the Redirect component
vi.mock("../Redirect", () => ({
  Redirect: vi.fn(({ to }) => <div data-testid="mock-redirect">{to}</div>),
}));

describe("InternalRedirect", () => {
  const renderComponent = (path: string) => {
    render(
      <MemoryRouter initialEntries={[path]}>
        <Routes>
          <Route
            path={routes.internalRedirect()}
            element={<InternalRedirect />}
          />
          =
        </Routes>
      </MemoryRouter>
    );
  };

  it("redirects to the correct path without search params", () => {
    renderComponent("/redirect/dashboard");
    expect(screen.getByTestId("mock-redirect").textContent).toBe("/dashboard");
  });

  it("redirects to the correct path with search params", () => {
    renderComponent("/redirect/profile?id=123&tab=settings");
    expect(screen.getByTestId("mock-redirect").textContent).toBe(
      "/profile?id=123&tab=settings"
    );
  });

  it("handles paths with multiple segments", () => {
    renderComponent("/redirect/users/edit/42");
    expect(screen.getByTestId("mock-redirect").textContent).toBe(
      "/users/edit/42"
    );
  });

  it("preserves complex search params", () => {
    renderComponent("/redirect/search?q=test%20query&filter[]=a&filter[]=b");
    expect(screen.getByTestId("mock-redirect").textContent).toBe(
      "/search?q=test%20query&filter[]=a&filter[]=b"
    );
  });

  it("handles redirect with empty path", () => {
    renderComponent("/redirect/");
    expect(screen.getByTestId("mock-redirect").textContent).toBe("/");
  });
});
