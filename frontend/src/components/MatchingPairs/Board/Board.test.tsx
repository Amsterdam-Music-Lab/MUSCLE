/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, expect, test } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import Board from "./Board";
import styles from "./Board.module.scss";

describe("Matching Pairs Board", () => {
  test("renders all children in slots", () => {
    const { container } = render(
      <Board columns={3}>
        <div data-testid="child-1" />
        <div data-testid="child-2" />
      </Board>
    );

    const slots = container.querySelectorAll(`.${styles.slot}`);
    expect(slots.length).toBe(2);
    expect(slots[0].querySelector('[data-testid="child-1"]')).toBeTruthy();
    expect(slots[1].querySelector('[data-testid="child-2"]')).toBeTruthy();
  });

  test("applies custom className to outer container", () => {
    const { container } = render(
      <Board columns={4} className="my-custom-class" />
    );
    expect(container.firstChild).toHaveClass("my-custom-class");
  });

  test("applies column count as CSS variable", () => {
    const { container } = render(<Board columns={5} />);
    const grid = container.querySelector(".square-grid") as HTMLElement;
    expect(grid?.style.getPropertyValue("--columns")).toBe("5");
  });
});
