/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import type { HTMLAttributes } from "react";
import { describe, expect, it } from "vitest";
import { screen } from "@testing-library/react";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import Board, { SlotProps } from "./Board";
import { getColoredSlots } from "./utils.tsx";
import styles from "./Board.module.scss";

describe("Matching Pairs Board", () => {
  it("renders all children in slots", () => {
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

  it("applies custom className to outer container", () => {
    const { container } = render(
      <Board columns={4} className="my-custom-class" />
    );
    expect(container.firstChild).toHaveClass("my-custom-class");
  });

  it("applies column count as CSS variable", () => {
    const { container } = render(<Board columns={5} />);
    const grid = container.querySelector(".square-grid") as HTMLElement;
    expect(grid?.style.getPropertyValue("--columns")).toBe("5");
  });

  it("renders children with slot props correctly", () => {
    render(
      <Board columns={4}>
        {[
          [
            <div key="1">A</div>,
            {
              "data-testid": "slot-1",
              style: { backgroundColor: "red" },
            } as HTMLAttributes<HTMLDivElement>,
          ],
          [
            <div key="2">B</div>,
            {
              "data-testid": "slot-2",
              style: { backgroundColor: "blue" },
            } as HTMLAttributes<HTMLDivElement>,
          ],
        ]}
      </Board>
    );
    const slot1 = screen.getByTestId("slot-1");
    const slot2 = screen.getByTestId("slot-2");

    expect(slot1).toHaveStyle("background-color: red");
    expect(slot1).toHaveTextContent("A");
    expect(slot2).toHaveStyle("background-color: blue");
    expect(slot2).toHaveTextContent("B");
  });

  it("applies slotProps correctly to each slot", () => {
    const children = getColoredSlots(9);
    render(<Board columns={3}>{children}</Board>);

    // Check that slot styles were applied
    children.forEach((_, index) => {
      const slot = screen.getByTestId(`slot-${index}`);
      const expectedColor = `hsl(${(index / 9) * 360}, 100%, 50%)`;
      expect(slot).toHaveStyle({ borderColor: expectedColor });
    });

    // Also check that child content is rendered
    children.forEach((_, index) => {
      expect(screen.getByTestId(`card-${index}`)).toBeInTheDocument();
    });
  });

  it("applies the invisible class when slotProps.invisible is true", () => {
    render(
      <Board columns={2}>
        {[
          [
            <div data-testid="card-0">Card 0</div>,
            { invisible: true } as SlotProps,
          ],
        ]}
      </Board>
    );

    const slot = screen.getByTestId("card-0").parentElement;
    expect(slot).toHaveClass(styles.invisible);
  });

  it("does not apply the invisible class when slotProps.invisible is false", () => {
    render(
      <Board columns={2}>
        {[
          [
            <div data-testid="card-1">Card 1</div>,
            { invisible: false } as SlotProps,
          ],
        ]}
      </Board>
    );

    const slot = screen.getByTestId("card-1").parentElement;
    expect(slot).not.toHaveClass(styles.invisible);
  });
});
