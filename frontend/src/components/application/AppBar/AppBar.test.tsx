/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { BrowserRouter as Router } from "react-router-dom";
import { vi, describe, beforeEach, it, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import AppBar from "./AppBar";

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

  it.skip("renders logo as Link for relative URL", () => {
    const { getByLabelText } = render(<AppBar title="Test Title" />, {
      wrapper: Router,
    });
    const logo = getByLabelText("Logo");
    expect(logo.tagName).toBe("A");
    expect(logo.getAttribute("href")).toBe(BASE_URL);
  });

  it.skip("renders logo as an a-element for absolute URL", () => {
    const { getByLabelText } = render(<AppBar title="Test Title" />, {
      wrapper: Router,
    });
    const logo = getByLabelText("Logo");
    expect(logo.tagName).toBe("A");
    expect(logo.getAttribute("href")).toBe(BASE_URL);
  });
});
