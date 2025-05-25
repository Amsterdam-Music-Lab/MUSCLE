/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { vi, describe, expect, test } from "vitest";
import { screen } from "@testing-library/dom";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";

import AudioCard from "./AudioCard";
import styles from "./AudioCard.module.scss";

vi.mock("@/components/play", () => ({
  __esModule: true,
  Spectrum: (props: any) => (
    <div data-testid="spectrum" data-props={JSON.stringify(props)}>
      Mock Spectrum
    </div>
  ),
}));

describe("Matching Pairs Audio Card", () => {
  test("renders AudioCard component", () => {
    const { container } = render(<AudioCard />);
    const component = container.querySelector(`.${styles.audio}`);
    expect(component).toBeInTheDocument();
  });

  test("applies custom className", () => {
    const { container } = render(<AudioCard className="my-class" />);
    expect(container.firstChild).toHaveClass("my-class");
  });

  test("passes running, bars, random and interval to Histogram", () => {
    render(
      <AudioCard
        flipped={true}
        running={true}
        bars={8}
        random={false}
        interval={500}
      />
    );
    const el = screen.getByTestId("spectrum");
    const props = JSON.parse(el.getAttribute("data-props") || "{}");

    expect(props.running).toBe(true);
    expect(props.bars).toBe(8);
    expect(props.random).toBe(false);
    expect(props.interval).toBe(500);
  });
});
