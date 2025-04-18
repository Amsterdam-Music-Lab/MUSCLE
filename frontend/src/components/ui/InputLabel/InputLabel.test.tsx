/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, expect, it, vi } from "vitest";
import { screen } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import InputLabel from "./InputLabel";

describe("Button component", () => {
  it("renders children", () => {
    render(<InputLabel>Username</InputLabel>);
    expect(screen.getByText("Username")).toBeInTheDocument();
  });

  it("sets the htmlFor attribute", () => {
    render(<InputLabel htmlFor="email">Email</InputLabel>);
    const label = screen.getByText("Email").closest("label");
    expect(label).toHaveAttribute("for", "email");
  });

  it("applies custom className", () => {
    render(<InputLabel className="custom-class">Label</InputLabel>);
    const label = screen.getByText("Label").closest("label");
    expect(label).toHaveClass("custom-class");
  });

  it("applies variant class", () => {
    render(<InputLabel variant="primary">Name</InputLabel>);
    const span = screen.getByText("Name");
    expect(span).toHaveClass("text-fill-primary");
  });

  it("forwards other props to label element", () => {
    render(
      <InputLabel htmlFor="id" title="My label">
        Label text
      </InputLabel>
    );
    const label = screen.getByText("Label text").closest("label");
    expect(label).toHaveAttribute("title", "My label");
  });
});
