/**
 * Copyright (c) 2025 Amsterdam Music Lab
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */
import "@testing-library/jest-dom";
import { describe, expect, it } from "vitest";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import Cup from "./Cup";
import styles from "./Cup.module.scss";

describe("Cup Component", () => {
  it("renders with default props", () => {
    const { getByTestId } = render(<Cup />);
    const cup = getByTestId("cup");
    const text = getByTestId("cup-text");

    expect(cup).toBeInTheDocument();
    expect(cup.className).toContain("plastic"); // default type
    expect(text.textContent).toBe("Plastic"); // default label
  });

  it("renders with a specific type and label", () => {
    const { getByTestId } = render(<Cup type="gold" label="Gold Rank" />);

    const cup = getByTestId("cup");
    const text = getByTestId("cup-text");

    expect(cup.className).toContain("gold");
    expect(text.textContent).toBe("Gold Rank");
  });

  it("hides label if label is false", () => {
    const { queryByTestId } = render(<Cup label={false} />);
    expect(queryByTestId("cup-text")).toBeNull();
  });

  it("uses capitalized type as fallback label", () => {
    const { getByTestId } = render(<Cup type="silver" />);
    expect(getByTestId("cup-text").textContent).toBe("Silver");
  });

  it("applies custom radius as style", () => {
    const { getByTestId } = render(<Cup radius={200} />);
    const cup = getByTestId("cup");
    expect(
      (cup.parentElement as HTMLElement).style.getPropertyValue("--cup-radius")
    ).toBe("200px");
  });

  it("adds animate class when animate=true", () => {
    const { getByTestId } = render(<Cup animate={true} />);
    const wrapper = getByTestId("cup").parentElement!;
    expect(wrapper.className).toContain("animate");
  });

  it("does not add animate class when animate=false", () => {
    const { getByTestId } = render(<Cup animate={false} />);
    const wrapper = getByTestId("cup").parentElement!;
    expect(wrapper.className).not.toContain("animate");
  });

  it("renders halo (rays) when showHalo is true", () => {
    const { container } = render(<Cup showHalo={true} />);
    expect(container.querySelector(`.${styles.rays}`)).toBeTruthy();
  });

  it("does not render halo (rays) when showHalo is false", () => {
    const { container } = render(<Cup showHalo={false} />);
    expect(container.querySelector(`.${"rays"}`)).toBeFalsy();
  });

  it("renders label in lowercase when uppercase is false", () => {
    const { getByTestId } = render(<Cup label="gold rank" uppercase={false} />);
    const label = getByTestId("cup-text");
    expect(label.className).not.toContain("uppercase");
    expect(label.textContent).toBe("gold rank");
  });

  it("merges --cup-radius and custom style props", () => {
    const { getByTestId } = render(
      <Cup radius={200} style={{ backgroundColor: "red" }} />
    );

    const cupContainer = getByTestId("cup").parentElement as HTMLElement;

    expect(cupContainer.style.getPropertyValue("--cup-radius")).toBe("200px");
    expect(cupContainer.style.backgroundColor).toBe("red");
  });
});
