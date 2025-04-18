/**
 * Copyright (c) 2025 Bas Cornelissen
 * SPDX-License-Identifier: MIT
 *
 * This file is part of the MUSCLE project by Amsterdam Music Lab.
 * Licensed under the MIT License. See LICENSE file in the project root.
 */

import "@testing-library/jest-dom";
import { describe, expect, it, vi } from "vitest";
import { fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { renderWithProviders as render } from "@/util/testUtils/renderWithProviders";
import LinkButton, { isRelativeUrl } from "./LinkButton";
import buttonStyles from "../Button/Button.module.scss";

describe("LinkButton component", () => {
  it("renders as a Button when no link is provided", () => {
    const { getByTestId } = render(<LinkButton>Click me</LinkButton>);

    const button = getByTestId("button-link");
    expect(button.tagName).toBe("BUTTON");
    expect(button).toHaveTextContent("Click me");
  });

  it("renders as a React Router Link when a relative URL is provided", () => {
    const { getByTestId } = render(
      <MemoryRouter>
        <LinkButton link="/relative-path" variant="secondary">
          Go to page
        </LinkButton>
      </MemoryRouter>
    );

    const link = getByTestId("button-link");
    expect(link.tagName).toBe("A");
    expect(link).toHaveAttribute("href", "/redirect/relative-path");
    expect(link).toHaveTextContent("Go to page");
  });

  it("renders as an anchor tag when an absolute URL is provided", () => {
    const { getByTestId } = render(
      <LinkButton link="https://example.com">External Link</LinkButton>
    );

    const anchor = getByTestId("button-link");
    expect(anchor.tagName).toBe("A");
    expect(anchor).toHaveAttribute("href", "https://example.com");
    expect(anchor).toHaveAttribute("target", "_blank");
    expect(anchor).toHaveAttribute("rel", "noopener noreferrer");
    expect(anchor).toHaveTextContent("External Link");
  });

  it("applies the correct button classes", () => {
    const { getByTestId } = render(
      <LinkButton variant="primary" size="lg" rounded>
        Styled Button
      </LinkButton>
    );

    const button = getByTestId("button-link");
    expect(button).toHaveClass("fill-primary");
    expect(button).toHaveClass(buttonStyles.lg);
    expect(button).toHaveClass(buttonStyles.rounded);
  });

  it("calls the onClick handler when the button is clicked", () => {
    const handleClick = vi.fn();
    const { getByTestId } = render(
      <LinkButton onClick={handleClick}>Click me</LinkButton>
    );

    fireEvent.click(getByTestId("button-link"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("renders children correctly", () => {
    const { getByTestId } = render(
      <LinkButton>
        <span>Child Element</span>
      </LinkButton>
    );

    const button = getByTestId("button-link");
    expect(button).toContainHTML("<span>Child Element</span>");
  });

  it("correctly identifies relative URLs", () => {
    expect(isRelativeUrl("/relative-path")).toBe(true);
    expect(isRelativeUrl("https://example.com")).toBe(false);
    expect(isRelativeUrl("")).toBe(false);
  });

  it("applies custom class names", () => {
    const { getByTestId } = render(
      <LinkButton className="custom-class">Custom Button</LinkButton>
    );

    const button = getByTestId("button-link");
    expect(button).toHaveClass("custom-class");
  });

  it("is accessible and has the correct attributes", () => {
    const { getByTestId } = render(
      <LinkButton link="https://example.com" aria-label="External Link">
        External Link
      </LinkButton>
    );

    const anchor = getByTestId("button-link");
    expect(anchor).toHaveAttribute("aria-label", "External Link");
  });
});
