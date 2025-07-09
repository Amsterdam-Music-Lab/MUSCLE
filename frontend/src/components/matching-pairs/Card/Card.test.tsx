/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, expect, test } from "vitest";
import { screen } from "@testing-library/dom";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import Card from "./Card";
import styles from "./Card.module.scss";

describe("Matching Pairs Generic Card", () => {
  test("renders front when flipped is true", () => {
    render(<Card flipped />);
    expect(screen.getByTestId("front")).toBeInTheDocument();
    expect(screen.queryByTestId("back")).not.toBeInTheDocument();
  });

  test("renders back when flipped is false", () => {
    render(<Card flipped={false} />);
    expect(screen.getByTestId("back")).toBeInTheDocument();
    expect(screen.queryByTestId("front")).not.toBeInTheDocument();
  });

  test("applies flipped and disabled classes", () => {
    const { container } = render(<Card flipped disabled />);
    const card = container.querySelector('[data-testid="playing-card"]');
    expect(card).toHaveClass(styles.flipped);
    expect(card).toHaveClass(styles.disabled);
  });

  test("uses variantFront and variantBack when no children are provided", () => {
    render(<Card flipped={false} variantBack="secondary" />);
    const back = screen.getByTestId("back");
    expect(back).toHaveClass("fill-secondary");
  });

  test("renders custom Card.Front and Card.Back", () => {
    render(
      <Card flipped={true}>
        <Card.Front data-testid="custom-front">FRONT</Card.Front>
        <Card.Back data-testid="custom-back">BACK</Card.Back>
      </Card>
    );

    expect(screen.getByTestId("custom-front")).toBeInTheDocument();
    expect(screen.queryByTestId("custom-back")).not.toBeInTheDocument();
  });

  test("renders label inside default back if no children are provided", () => {
    render(<Card flipped={false} label="Test Label" />);
    expect(screen.getByText("Test Label")).toBeInTheDocument();
  });
});
