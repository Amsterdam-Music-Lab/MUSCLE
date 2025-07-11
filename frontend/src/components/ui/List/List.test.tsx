/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import "@testing-library/jest-dom";
import { describe, it, expect } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders.tsx";
import { screen } from "@testing-library/react";
import List from "./List";

describe("List", () => {
  it("renders all list items", () => {
    render(<List items={[{ content: "One" }, { content: "Two" }]} />);
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
  });

  it("renders an ordered list when ordered=true", () => {
    const { container } = render(
      <List items={[{ content: "Item" }]} ordered />
    );
    expect(container.querySelector("ol")).toBeInTheDocument();
  });

  it("renders an unordered list when ordered=false", () => {
    const { container } = render(
      <List items={[{ content: "Item" }]} ordered={false} />
    );
    expect(container.querySelector("ul")).toBeInTheDocument();
  });

  it("uses index as label when label is not provided", () => {
    render(<List items={[{ content: "Foo" }]} />);
    expect(screen.getByText("1")).toBeInTheDocument(); // index + 1
  });

  it("adds animation class when animate is true", () => {
    render(<List items={[{ content: "Item" }]} animate />);
    const li = screen.getByRole("listitem");
    expect(li.className).toMatch(/anim-/);
  });

  it("does not add animation class when animate is false", () => {
    render(<List items={[{ content: "Item" }]} animate={false} />);
    const li = screen.getByRole("listitem");
    expect(li.className).not.toMatch(/anim-/);
  });

  it("renders markdown content", () => {
    render(<List items={[{ content: "**Bold text**" }]} />);
    expect(screen.getByText("Bold text").tagName).toBe("STRONG");
  });

  it("applies correct animation delay style", () => {
    render(<List items={[{ content: "A" }, { content: "B" }]} delay={200} />);
    const lis = screen.getAllByRole("listitem");
    expect(lis[1]).toHaveStyle({ animationDelay: "200ms" });
  });
});
