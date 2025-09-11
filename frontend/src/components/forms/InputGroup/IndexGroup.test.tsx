/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, expect, it } from "vitest";
import { screen } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import InputGroup from "./InputGroup";

const MockChild = ({ variant }: { variant?: string }) => (
  <div data-testid="mock-child">{variant}</div>
);
MockChild.displayName = "MockChild";

describe("Button component", () => {
  it("renders children", () => {
    render(
      <InputGroup>
        <div data-testid="child">Hello</div>
      </InputGroup>
    );
    expect(screen.getByTestId("child")).toHaveTextContent("Hello");
  });

  it("applies custom className", () => {
    render(
      <InputGroup className="custom-class">
        <span />
      </InputGroup>
    );
    expect(screen.getByTestId("input-group")).toHaveClass("custom-class");
  });

  it("forwards variant to children when forwardVariant is true", () => {
    render(
      <InputGroup variant="primary">
        <MockChild />
      </InputGroup>
    );
    expect(screen.getByTestId("mock-child")).toHaveTextContent("primary");
  });

  it("does not forward variant when forwardVariant is false", () => {
    render(
      <InputGroup variant="primary" forwardVariant={false}>
        <MockChild />
      </InputGroup>
    );
    expect(screen.getByTestId("mock-child")).toHaveTextContent("");
  });

  it("ignores non-element children", () => {
    render(
      <InputGroup variant="primary">
        Text node
        <MockChild />
      </InputGroup>
    );
    expect(screen.getByText("Text node")).toBeInTheDocument();
    expect(screen.getByTestId("mock-child")).toHaveTextContent("primary");
  });
});
