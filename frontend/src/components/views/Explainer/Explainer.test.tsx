/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import { screen } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import { vi, describe, it, expect } from "vitest";

import Explainer from "./Explainer";

describe("Explainer Component", () => {
  const props = {
    instruction: "Some instruction",
    button_label: "Next",
    steps: [],
    onNext: vi.fn(),
    timer: 1,
  };

  it("renders with given props", () => {
    render(<Explainer {...props} />);
    expect(screen.getByTestId("explainer")).toBeTruthy();
  });

  it("renders the instruction message", async () => {
    render(<Explainer {...props} />);
    await screen.findByText("Some instruction");
  });
});
