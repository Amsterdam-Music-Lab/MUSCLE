/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import OptionField from "./OptionField";
import RadioField from "./RadioField";

const OPTIONS = [
  { value: "apple", label: "Apple" },
  { value: "banana", label: "Banana" },
  { value: "carrot", label: "Carrot", disabled: true },
];

describe("OptionField (alias for CheckboxField)", () => {
  it("renders all options with correct labels", () => {
    render(
      <OptionField
        type="checkbox"
        name="fruits"
        values={["apple"]}
        options={OPTIONS}
        onChange={() => {}}
      />
    );

    expect(screen.getByLabelText("Apple")).toBeInTheDocument();
    expect(screen.getByLabelText("Banana")).toBeInTheDocument();
    expect(screen.getByLabelText("Carrot")).toBeDisabled();
  });

  it("calls onChange with added value when checking", () => {
    const onChange = vi.fn();
    render(
      <OptionField
        type="checkbox"
        name="fruits"
        values={[]}
        options={OPTIONS}
        onChange={onChange}
      />
    );

    const banana = screen.getByLabelText("Banana");
    fireEvent.click(banana);

    expect(onChange).toHaveBeenCalledWith(["banana"]);
  });

  it("calls onChange with removed value when unchecking", () => {
    const onChange = vi.fn();
    render(
      <OptionField
        type="checkbox"
        name="fruits"
        values={["banana"]}
        options={OPTIONS}
        onChange={onChange}
      />
    );

    const banana = screen.getByLabelText("Banana");
    fireEvent.click(banana);

    expect(onChange).toHaveBeenCalledWith([]);
  });

  it("displays error message and ARIA attributes", () => {
    render(
      <OptionField
        type="checkbox"
        name="fruits"
        values={[]}
        options={OPTIONS}
        onChange={() => {}}
        error="You must select at least one fruit."
      />
    );

    const fieldset = screen.getByRole("group");
    expect(fieldset).toHaveAttribute("aria-describedby", "fruits-error");
    expect(fieldset).toHaveAttribute("aria-invalid", "true");

    expect(
      screen.getByText("You must select at least one fruit.")
    ).toBeInTheDocument();
  });
});

describe("RadioField", () => {
  it("selects only one value at a time", () => {
    const onChange = vi.fn();
    render(
      <RadioField
        type="radio"
        name="fruit"
        value="apple"
        options={OPTIONS}
        onChange={onChange}
      />
    );

    const banana = screen.getByLabelText("Banana");
    fireEvent.click(banana);

    expect(onChange).toHaveBeenCalledWith("banana");
  });
});
