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
import NarrowLayout from "./NarrowLayout";

describe("NarrowLayout", () => {
  it("renders children and applies maxWidth style", () => {
    const { getByText, container } = render(
      <NarrowLayout maxWidth={400}>Hello World</NarrowLayout>
    );
    // Check children
    expect(getByText("Hello World")).toBeInTheDocument();
    // Check style
    const div = container.firstChild as HTMLElement;
    expect(div.style.getPropertyValue("--narrow-layout-max-width")).toBe(
      "400px"
    );
  });
});
