/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { createRef } from "react";
import { describe, expect, it, vi } from "vitest";
import { screen, fireEvent } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import Input from "./Input";

describe("Button component", () => {
  it("renders with initial value", () => {
    render(<Input value="Hello" />);
    expect(screen.getByRole("textbox")).toHaveValue("Hello");
  });

  it("calls onChange and updates internal state", () => {
    const handleChange = vi.fn();
    render(<Input value="" onChange={handleChange} />);

    const input = screen.getByRole("textbox");
    fireEvent.change(input, { target: { value: "Updated" } });

    expect(handleChange).toHaveBeenCalled();
    expect(input).toHaveValue("Updated");
  });

  it("applies custom className", () => {
    render(<Input className="custom-class" />);
    expect(screen.getByRole("textbox")).toHaveClass("custom-class");
  });

  it("accepts placeholder and disabled props", () => {
    render(<Input placeholder="Type here" disabled />);
    const input = screen.getByPlaceholderText("Type here");
    expect(input).toBeDisabled();
  });

  it("forwards ref to the input element", () => {
    const ref = createRef<HTMLInputElement>();
    render(<Input ref={ref} />);
    expect(ref.current).toBeInstanceOf(HTMLInputElement);
  });
});
